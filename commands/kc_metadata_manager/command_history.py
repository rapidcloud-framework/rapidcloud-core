__author__ = "Igor Royzis"
__license__ = "MIT"


import datetime
import logging
from boto3.dynamodb.conditions import Key, Attr

from commands.colors import colors
from commands.kc_metadata_manager.aws_metadata import Metadata

class CommandHistory(Metadata):

    TABLE_NAME = 'command_history'
    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)

    def __init__(self, args):
        super().__init__(args)


    def get_command(self, timestamp):
        return self.get_dynamodb_resource().Table(self.TABLE_NAME).query(
            KeyConditionExpression=Key('timestamp').eq(timestamp)
        )['Items'][0]


    def construct_command(self, command):
        c = command['command'] if command['command'] else ''
        cmd_raw = f"{command['phase']} {c} "
        cmd = f"$ {colors.WARNING}kc {command['phase']} {c}{colors.ENDC} "
        for arg, value in command['command_arguments'].items():
            if value and arg not in ('feature','command'):
                if hasattr(super().get_args(), arg) and arg not in ('datalake','data_lake_fqn','output_folder_path','aws_region'):
                    # value = '"' + value + '"' if ' ' in value else value
                    cmd += f"{colors.OKBLUE}--{arg}{colors.ENDC} {value} "
                    cmd_raw +=f"--{arg} {value} "
        
        return {
            "cmd_raw": cmd_raw,
            "timestamp": command['timestamp'],
            "cmd": cmd
        }



    def get_commands_for_current_env(self):
        resources = super().get_all_resources()
        if self.args.verbose:
            print(f"{len(resources)} resources for current environment")
        if not resources:
            return []
        resources = sorted(resources, key=lambda x: x['timestamp'])
        
        timestamp = resources[0]['timestamp']
        date_time_obj = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f') - datetime.timedelta(seconds=60)
        timestamp = date_time_obj.strftime("%Y-%m-%d %H:%M:%S.%f")

        extra_filters = Attr('timestamp').gte(timestamp)
        module = self.args.module
        if module is not None:
            extra_filters = extra_filters & Attr('phase').eq(module)
        history = super().get_all_resources('command_history', extra_filters=extra_filters)
        if self.args.verbose:
            print(f"{len(history)} command executions")

        if not history:
            return []
        
        commands = {}
        history = sorted(history, key=lambda x: x['timestamp'])
        for command in history:
            c = command['command'] if command['command'] else ''
            cmd_raw = f"{command['phase']} {c} "
            command_info = self.construct_command(command)
            command_info['user'] = command['user']
            commands[command_info['cmd_raw']] = command_info

        commands_sorted = []
        for cmd_raw, values in commands.items():
            commands_sorted.append({
                "id": values['timestamp'].replace('-','').replace(':','').replace(' ','').replace('.',''),
                "raw": cmd_raw,
                "timestamp": values['timestamp'][0:values['timestamp'].rfind('.')],
                "cmd": values['cmd'],
                "user": values['user']
            })

        commands_sorted = sorted(commands_sorted,  key=lambda x: x['timestamp'])
        for_diagram = []
        if self.args.verbose:
            print(f"{len(commands_sorted)} sorted")
        for cmd in commands_sorted:
            for_diagram.append(cmd['raw'])
            print(f"\nID [{cmd['id']}] {cmd['timestamp']} [{cmd['user']}]\n{cmd['cmd']}")

        return for_diagram
