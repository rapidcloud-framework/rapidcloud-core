#!/usr/bin/env python3

__author__ = "Igor Royzis"
__copyright__ = "Copyright 2023, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import json
import logging
import os
from threading import Thread
import time
import traceback
from datetime import datetime
from commands import general_utils

from server.utils.server_helper import ServerHelper

class CliHelper(ServerHelper):

    logger = logging.getLogger(__name__)

    def __init__(self, args, app_mode):
        super().__init__(args, app_mode)
        self.args = args


    def get_cli_arg_value(self, v):
        if v is None or str(v) == "":
            return "\"\""
        elif isinstance(v, str) and v.strip():
            if '$' not in v:
                return f"\"{v}\""
            else:
                return f"'{v}'"
        elif isinstance(v, list):
            v = json.dumps(v, default=str).replace('"', '\\"')
            return f"\"{v}\""
        elif isinstance(v, dict):
            v = json.dumps(v, default=str).replace('"', '\\"')
            return f"\"{v}\""
        else:
            return str(v).replace('"', '\\"')


    def get_dyn_arg_value(self, v):
        if v is None or str(v) == "":
            return ""
        elif isinstance(v, str) and v.strip():
            if '$' not in v:
                return v
            else:
                return v
        elif isinstance(v, list):
            v = json.dumps(v, default=str).replace('"', '\\"')
            return v
        elif isinstance(v, dict):
            v = json.dumps(v, default=str).replace('"', '\\"')
            return v
        else:
            return str(v).replace('"', '\\"')


    def gen_command_from_metadata(self, metadata):
        command = metadata['command'] if 'command' in metadata else ""
        cmd = [f"kc {metadata['module']} {command}"]
        for k,v in metadata['params'].items():
            cmd.append(f"--{k} {self.get_cli_arg_value(v)}")
        cmd.append("--no-prompt")
        return " ".join(cmd)


    def parse_command(self, request, region):
        cloud = general_utils.get_cloud_from_args(request.args).lower()
        dyn_args = {
            "feature": "",
            "args": {
                "cloud": cloud
            }
        }    

        body = request.json
        cmd = [f"export AWS_DEFAULT_REGION={region}; ./kc"]
        
        if 'phase' in body:
            dyn_args["feature"] = body['phase']
            cmd.append(body['phase'])
            if body['phase'] == 'undo-command':
                dyn_args["args"]["id"] = body['cmd_id']
                cmd.append(f"--id {body['cmd_id']}")
                return " ".join(cmd), dyn_args

        if 'command' in body:
            dyn_args["command"] = body['command']
            cmd.append(body['command'])

        dyn_args["args"]["mode"] = "console"
        cmd.append("--mode console")

        for k,v in body.items():
            if k not in ('phase', 'command', 'cli'):
                dyn_args["args"][k] = self.get_dyn_arg_value(v)
                cmd.append(f"--{k} {self.get_cli_arg_value(v)}")
        return " ".join(cmd), dyn_args


    def post_command(self, session, request, locked_environments, kc_exec):
        cmd, dyn_args = self.parse_command(request, session["region"])
        if cmd:
            cloud = session["cloud"]
            email = session["email"]
            dyn_args['mode'] = 'console'
            kc_results = self.kc(email, dyn_args, locked_environments, kc_exec)

            if not os.path.exists("./logs"):
                os.makedirs("./logs")

            with open(f"./logs/latest.log", 'w') as kc_results_file:
                kc_results_file.write(json.dumps(kc_results, indent=2, default=str))

            # refresh status csv
            if 'refresh_status' in request.json and request.json['refresh_status']:
                Thread(target=self.kc_build_and_call, args=(cloud, email, request.json['env'],locked_environments, kc_exec,"status",)).start()

            return {
                "log_file": f"theia_{int(round(time.time() * 1000))}.log", 
                "cmd": cmd
            }
        else:
            return {"log_file": "ERROR: Command cannot be parsed"}


    def kc(self, email, dyn_args, locked_environments, kc_exec):
        try:
            if "env" in dyn_args["args"]:
                env = dyn_args["args"]["env"]
            else:
                env = "any"
            if env in locked_environments:
                locked_msg = f"{env} is locked by {locked_environments[env]['email']}"
                self.logger.info(locked_msg)
                return {
                    "error": locked_msg
                }
            
            self.lock_env(email, env, locked_environments, dyn_args)
            dyn_args["current_session_email"] = email
            results = kc_exec(dyn_args)
            self.unlock_env(env, locked_environments)
            return results

        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
            self.unlock_env(env, locked_environments)
            return {
                "error": e
            }
        

    def kc_build_and_call(self, cloud, email, env, locked_environments, kc_exec, module, command=None):
        try:
            dyn_args = {
                "cloud": cloud,
                "current_session_email": email,
                "feature": module,
                "command": command,
                "args": {
                    "env": env,
                    "mode": "console",
                    "quiet": True
                },
                'mode': 'console'
            }
            return self.kc(email, dyn_args, locked_environments, kc_exec)
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
            return None


    def lock_env(self, email, env, locked_environments, dyn_args):
        self.logger.info(f"locking {env}")
        locked_environments[env] = {
            "email": email,
            "command": f"kc {dyn_args.get('feature', '')} {dyn_args.get('command', '')}".strip(),
            "timestamp": str(datetime.now())
        }
        self.logger.info(f"locked_environments: {json.dumps(locked_environments, indent=2)}")


    def unlock_env(self, env, locked_environments):
        self.logger.info(f"unlocking {env}")
        locked_environments.pop(env)
        self.logger.info(f"locked_environments: {json.dumps(locked_environments, indent=2)}")

