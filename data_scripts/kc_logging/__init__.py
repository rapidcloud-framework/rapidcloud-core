__copyright__ = "Copyright 2023, Kinect Consulting"
__license__ = "Commercial"

import sys
import datetime
import json
import boto3


class Logger:
    def __init__(self, source_process_name=None, timestamp_format="%Y-%m-%d %H:%M:%S"):
        self._source_process_name = source_process_name
        self._timestamp_format = timestamp_format

    def log(self, log_severity=None, log_detail=None, **kwargs):

        ##DECLARATION SECTION
        functionID = sys._getframe().f_code.co_name

        try:
            log_message = {}
            standard_fields = {
                "source_process_name": self._source_process_name,
                "log_timestamp_utc": datetime.datetime.utcnow().strftime(
                    self._timestamp_format
                ),
                "log_severity": log_severity,
                "log_detail": log_detail,
            }
            for standard_key in standard_fields:
                if standard_fields[standard_key] is not None:
                    log_message[standard_key] = standard_fields[standard_key]
            for arg_key in kwargs:
                if kwargs[arg_key] is not None:
                    log_message[arg_key] = kwargs[arg_key]

            log_message = json.dumps(log_message, indent=2)

            print(log_message)

        except Exception as e:
            msg = e.args
            exceptionMessage = f"Exception Occurred Inside this method {functionID} --> Here is the exception Message {msg}"
            print(f"Error: {exceptionMessage}")
            raise Exception(exceptionMessage)
