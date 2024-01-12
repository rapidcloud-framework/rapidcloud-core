__author__ = "Igor Royzis"
__copyright__ = "Copyright 2020, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

from datetime import datetime
import logging
from boto3.dynamodb.conditions import Key, Attr

from commands.kc_metadata_manager.aws_metadata import Metadata

class TargetDatabase(Metadata):

    TABLE_NAME = 'target_database'
    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)


    def __init__(self, args):
        super().__init__(args)
        self.args = args
        self.env = super().get_env()


    def save_target_rdbms(self):
        dbtype = self.args.type
        engine = self.args.engine
        name = self.args.name
        multi_az = self.args.multi_az in ('true', 'yes')
        database_name = self.args.database_name

        fqn = f"{self.env}_{dbtype}_{engine}_{name}"
        
        if dbtype == 'rds':
            if engine == 'mysql':
                resource_type = 'rds_mysql_instance'
            elif engine == 'postgres':
                resource_type = 'rds_postgresql_instance'                
        elif dbtype == 'aurora':
            if engine == 'mysql':
                resource_type = 'aurora_mysql_instance'
            elif engine == 'postgres':
                resource_type = 'aurora_postgresql_instance'

        params = super().get_db_params(dbtype, engine, resource_type, multi_az, name, database_name)

        item={
            'fqn': fqn, 
            'profile': self.env, 
            'name': name, 
            'type': dbtype,
            'engine': engine,
            'resource_type': resource_type,
            'multi_az': multi_az,
            'database_name': database_name,
            'timestamp': str(datetime.now())
        }
        super().put_item(self.TABLE_NAME, item)
        super().build_metadata_item(item, "metadata")

        super().save_password(self.env, resource_type, name, '')

        super().add_aws_resource(resource_type, name, params)

        # sns_topics
        super().add_aws_resource('sns_topic', 'transformations', params)
        super().add_aws_resource('sns_topic', 'publishing', params)

        # lambda function (may or may not be used for specific use case)
        env_vars = {"PROFILE": self.env}
        layers = {"10": f"{self.env}_lambda_layer_awswrangler"}
        params = super().get_lambda_function_params(env_vars, layers)
        params['source_path'] = "default_lambda_template"
        params['immutable'] = True
        super().add_aws_resource("lambda_function", "run_publishing", params)

        # sns_topic_subscription
        params = super().get_sns_topic_subscription_params("transformations", "run_publishing")
        super().add_aws_resource('sns_topic_subscription', 'transformations', params)



    def get_all_target_databases(self):
        return super().get_dynamodb_resource().Table('target_database').scan(        
            FilterExpression=Attr('profile').eq(self.env) 
        )['Items']


    def get_target_database(self, fqn):
        return super().get_dynamodb_resource().Table('target_database').query(
            KeyConditionExpression=Key('fqn').eq(fqn)
        )['Items'][0]
