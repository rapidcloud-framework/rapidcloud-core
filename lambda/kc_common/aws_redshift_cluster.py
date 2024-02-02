__author__ = "Igor Royzis"
__license__ = "MIT"


import json
import boto3
import logging
import os
from arnparse import arnparse
from kc_common.aws_worker import AwsWorker

logger = logging.getLogger("metadata")
logger.setLevel(logging.INFO)

PROFILE = os.environ['PROFILE']

session = boto3.Session()
redshift_client = session.client('redshift')

class Worker(AwsWorker):

    def __init__(self):
        super().__init__()

    def get_service_name(self):
        return "Redshift"

    def pause(self, arn):
        try:
            cluster_id = arnparse(arn).resource
            resp = redshift_client.pause_cluster(
                ClusterIdentifier=cluster_id
            )
            logger.info(json.dumps(resp, indent=2, default=str))
        except Exception as e:
            logger.error(e)


    def resume(self, arn, details=None, tf_state=None):
        try:
            cluster_id = arnparse(arn).resource
            resp = redshift_client.resume_cluster(
                ClusterIdentifier=cluster_id
            )
            logger.info(json.dumps(resp, indent=2, default=str))
        except Exception as e:
            logger.error(e)


    def status(self, arn):
        try:
            cluster_id = arnparse(arn).resource
            resp = redshift_client.describe_clusters(
                ClusterIdentifier=cluster_id
            )
            # print(json.dumps(resp, indent=2, default=str))
            if "Clusters" in resp:
                details = resp["Clusters"][0]
                return details["ClusterStatus"], details
        except Exception as e:
            logger.error(e)
        return "?",{}
