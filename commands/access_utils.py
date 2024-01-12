__author__ = "Igor Royzis"
__copyright__ = "Copyright 2023, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import logging
from commands.colors import colors

logger = logging.getLogger(__name__)

ALLOW_MODULES_LIST = [
    "agree_terms",
    "console",
    "dynamodb_scan",
    "help",
    "status"
]

ALLOW_COMMANDS_LIST = [
    "init.set-env"
]

def allow_command(module, command, permissions):
    cmd = f"kc {module}"
    if command:
        cmd += f" {command}"

    print(f"Verifying permission for `{cmd}`:", end=" ")
    cmd = f"{module}.{command}"
    allow = False
    
    if module in ALLOW_MODULES_LIST or cmd in ALLOW_COMMANDS_LIST or permissions.get("access_all", "none") == "read-write" or permissions.get(f"access_{module}", "none") == "read-write":
        allow = True

    if allow:
        print(f"{colors.OKGREEN}ok{colors.ENDC}")
    else:
        print(f"{colors.FAIL}you don't have permission to execute `{cmd}`{colors.ENDC}")
    print("")

    return allow
