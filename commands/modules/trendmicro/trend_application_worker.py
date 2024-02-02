__author__ = "Igor Royzis"
__license__ = "MIT"


import json
import logging
from boto3.dynamodb.conditions import Key, Attr

from commands.modules import pause
import commands.modules.trendmicro.trend_api as trend_api


class TrendApplicationSecurityWorker(object):

    logger = logging.getLogger(__name__)

    def __init__(self, module):
        self.module = module
        self.args = module.args
        self.env = module.env
        self.metadata_table = self.module.get_dynamodb_resource().Table("metadata")


    def application_create_group(self, metadata=None):
        GROUP_NAME = self.args.name.upper()
        GROUP_NAME_FULL = f"{self.env}_{GROUP_NAME}".upper()
        self.logger.info(f"Creating or updating group {GROUP_NAME_FULL}")

        # get existing group
        result = trend_api.call_api(self.env, trend_api.APPLICATION_SECURITY, "GET", "accounts/groups", boto3_session=self.get_boto3_session())
        application_group = None
        for group in result:
            if GROUP_NAME_FULL == group['name']:
                application_group = group
                break
        self.logger.info("GROUP INFO:")
        self.logger.info(json.dumps(application_group, indent=2, default=str))
        pause(self.args)

        # create group
        if application_group is None:
            params = {
                "name": GROUP_NAME_FULL
            }
            application_group = trend_api.call_api(self.env, trend_api.APPLICATION_SECURITY, "POST", "accounts/groups", params, boto3_session=self.get_boto3_session())
            self.logger.info("GROUP INFO:")
            self.logger.info(json.dumps(application_group, indent=2, default=str))
            pause(self.args)

            # get group settings
            settings = trend_api.call_api(self.env, trend_api.APPLICATION_SECURITY, "GET", f"accounts/groups/{application_group['group_id']}/settings", boto3_session=self.get_boto3_session())
        else:
            self.logger.info(f"Group {GROUP_NAME_FULL} already exists")
            application_group = trend_api.call_api(self.env, trend_api.APPLICATION_SECURITY, "GET", f"accounts/groups/{application_group['group_id']}", boto3_session=self.get_boto3_session())
            settings = application_group['settings']
            pause(self.args)

        # save group secret in secrets manager
        secret = {
            "key": application_group['credentials']['key'],
            "secret": application_group['credentials']['secret']
        }
        self.module.save_secret(self.env, "trendmicro_app_security_group_secret", GROUP_NAME, json.dumps(secret))

        # update metadata  
        fqn = f"{self.env}_trendmicro_as_group_{self.args.name}"
        self.logger.info(f"fqn: {fqn}")
        metadata = self.metadata_table.query(KeyConditionExpression=Key('profile').eq(self.env) & Key('fqn').eq(fqn))['Items'][0]
        self.logger.info(json.dumps(metadata, indent=2, default=str))
        metadata['params']['trendmicro_group_secret'] = f"{self.env}/trendmicro_app_security_group_secret/{GROUP_NAME}"
        self.metadata_table.put_item(Item=metadata)        

        self.logger.info("SETTINGS:")
        self.logger.info(json.dumps(settings, indent=2, default=str))
        pause(self.args)

        # update group settings
        for setting, value in settings.items():
            settings[setting] = getattr(self.args, f"trendmicro_{setting}")
        self.logger.info(json.dumps(settings, indent=2, default=str))
        result = trend_api.call_api(self.env, trend_api.APPLICATION_SECURITY, "PUT", f"accounts/groups/{application_group['group_id']}/settings", params=settings, boto3_session=self.get_boto3_session())
        self.logger.info("SETTINGS UPDATED:")
        self.logger.info(json.dumps(result, indent=2, default=str))
