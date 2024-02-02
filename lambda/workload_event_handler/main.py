__author__ = "Igor Royzis"
__license__ = "MIT"


import json
import logging
import os
import sys

from kc_common import aws_workload

logging.basicConfig(level=logging.INFO, format=f'%(asctime)s %(levelname)-5s %(name)-39s:  %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

PROFILE = os.environ.get('PROFILE')


def lambda_handler(event, context):
    logger.info(json.dumps(event, indent=2, default=str))
    
    if "action" in event and event["action"] in ["pause", "resume"]:
        aws_workload.pause_or_resume(event)


def main():
    # export PROFILE=kc_100_qa
    # export LAMBDA_TASK_ROOT=./workload_event_handler
    # python -m workload_event_handler.main manual pause aurora verbose
    type = sys.argv[1]
    action = sys.argv[2]
    details = sys.argv[3]
    verbose = sys.argv[4]
    if type == "manual":
        event = {
            "action": action,
            "resource_types": details
        }
    else:
        event = {
            "action": action,
            "schedule_name": details
        }
    if verbose == "verbose":
        event['verbose'] = True
    lambda_handler(event, '')

if __name__ == "__main__":
    main()