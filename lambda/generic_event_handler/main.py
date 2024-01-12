__author__ = "Igor Royzis"
__copyright__ = "Copyright 2022, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import json
import logging
import os
import rc_cloudformation
import rc_trendmicro
import rc_ec2

logging.basicConfig(level=logging.INFO, format=f'%(asctime)s %(levelname)-5s %(name)-39s:  %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

PROFILE = os.environ.get('PROFILE')

def lambda_handler(event, context):
    logger.info(json.dumps(event, indent=2, default=str))
    
    if "source" in event and event["source"] == "aws.cloudformation":
        rc_cloudformation.handle_cloudformation_event(event)
    
    elif "source" in event and event["source"] == "aws.ec2":
        rc_ec2.handle_ec2_event(event)
    
    elif "rapidcloud_action" in event and event["rapidcloud_action"] == "rc_trendmicro.deploy_filestorage_stack":
        stack_name = event["stack_name"]
        cf_stack = event["cf_stack"]
        rc_trendmicro.deploy_filestorage_stack(stack_name, cf_stack)
    


# TEST
if __name__ == "__main__":
    print("testing...")
    # set up test variables here
    # ...

    # if sys.argv[1] == 'scanner':
    #     event = scanner
    # elif sys.argv[1] == 'storage':
    #     event = storage
    # elif sys.argv[1] == 'storage2':
    #     event = storage2
    # elif sys.argv[1] == 'all':
    #     event = all
    # elif sys.argv[1] == 'ec2':
    #     event = ec2
    # event['pause'] = sys.argv[2]
    # lambda_handler(event, None)
