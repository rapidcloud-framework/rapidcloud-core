__license__ = "MIT"

import sys
import datetime
import json
import boto3
from   data_scripts.kc_logging import Logger


class Notification:
    def __init__(self, notification_type="sns", aws_region="us-east-1"):
        self.notification_type = notification_type
        self.aws_region = aws_region

    def sendNotification(self, sns_topic, message, subject=None):

        ##DECLARATION SECTION
        functionID = sys._getframe().f_code.co_name

        self.logger = Logger(functionID)
        self.logger.log("INFO", f"Inside method: {functionID}")

        try:
            # Create an SNS client
            snsClient = boto3.client(
                self.notification_type, region_name=self.aws_region
            )
            # Publish a message
            if subject is not None:
                response = snsClient.publish(
                    TopicArn=sns_topic, Message=message, Subject=subject
                )
            else:
                response = snsClient.publish(TopicArn=sns_topic, Message=message)

        except Exception as e:
            msg = e.args
            exceptionMessage = f"Exception Occurred Inside this method {functionID} --> Here is the exception Message {msg}"
            self.logger.log("ERROR", exceptionMessage)
            raise Exception(exceptionMessage)
