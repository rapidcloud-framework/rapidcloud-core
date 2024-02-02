__author__ = "agarciaortiz"

from commands.kc_metadata_manager.aws_metadata import Metadata
import traceback

class ModuleMetadata(Metadata):

    def __init__(self, args):
        super().__init__(args)
        self.args = args

        # boto3
        self.boto3_session = super().get_boto3_session()

        # use boto3 clients or resources as follows
        # s3_client = self.boto3_session.client("s3")
        # dynamodb_res = self.boto3_session.resource("dynamodb")


    def get_common_params(self):
        return {
            "node_type": self.args.elasticache_node_type,
            "parameter_group_name": self.args.elasticache_parameter_group_name,
            "apply_immediately": "true" if self.args.elasticache_apply_immediately.lower() in ["yes", "true"] else "false",
            "engine_version": self.args.elasticache_engine_version,
            "maintenance_window": self.args.elasticache_maintenance_window,
            "notification_topic_arn": self.args.elasticache_notification_topic_arn,
            "replication_group_id": self.args.elasticache_replication_group_id,
            "security_group_ids": self.comma_separated_param_to_list(self.args.elasticache_security_group_ids),
            "subnet_ids": self.comma_separated_param_to_list(self.args.elasticache_subnet_ids),
        }

    def create_redis_cluster(self, metadata=None):
        super().delete_infra_metadata(name=self.args.name)

        params = {
            **self.get_common_params(),
            "availability_zone": self.args.elasticache_availability_zone,
            "final_snapshot_identifier": self.args.elasticache_final_snapshot_identifier,
            "log_destination": self.args.elasticache_log_destination,
            "log_destination_type": self.args.elasticache_log_destination_type,
            "log_format": self.args.elasticache_log_format,
            "log_type": self.args.elasticache_log_type
        }

        super().add_infra_resource("aws_elasticache_redis_cluster", self.args.name, params)

    def create_memcached_cluster(self, metadata=None):
        super().delete_infra_metadata(name=self.args.name)

        azs = self.comma_separated_param_to_list(self.args.elasticache_preferred_availability_zones)
        az_mode = "cross-az" if len(azs) > 1 else "single-az"
        
        if self.args.elasticache_num_cache_nodes and len(azs) < int(self.args.elasticache_num_cache_nodes):
            missing_zones = [azs[-1]] * (self.args.elasticache_num_cache_nodes-len(azs))
            azs += missing_zones

        params = {
            **self.get_common_params(),
            "az_mode": az_mode,
            "num_cache_nodes": self.args.elasticache_num_cache_nodes,
            "preferred_availability_zones": azs,
        }

        super().add_infra_resource("aws_elasticache_memcached_cluster", self.args.name, params)

    def create_replication_group(self, metadata=None):
        super().delete_infra_metadata(name=self.args.name)
        params = {
            **self.get_common_params(),
            "description": self.args.elasticache_description,
            "kms_key_name": self.args.elasticache_kms_key_name,
            "at_rest_encryption_enabled": "true" if self.args.elasticache_at_rest_encryption_enabled in ["yes", "true"] else "false",
            "transit_encryption_enabled": "true" if self.args.elasticache_transit_encryption_enabled in ["yes", "true"] else "false",
            "automatic_failover_enabled": "true" if self.args.elasticache_automatic_failover_enabled in ["yes", "true"] else "false",
            "multi_az_enabled": "true" if self.args.elasticache_multi_az_enabled in ["yes", "true"] else "false",
            "user_group_name": self.args.elasticache_user_group_name,
            "num_cache_clusters": self.args.elasticache_num_cache_clusters,
            "num_node_groups": self.args.elasticache_num_node_groups,
            "replicas_per_node_group": self.args.elasticache_replicas_per_node_group,
            "final_snapshot_identifier": self.args.elasticache_final_snapshot_identifier,
            "log_destination": self.args.elasticache_log_destination,
            "log_destination_type": self.args.elasticache_log_destination_type,
            "log_format": self.args.elasticache_log_format,
            "log_type": self.args.elasticache_log_type
        }

        super().add_infra_resource("aws_elasticache_replication_group", self.args.name, params)

    def create_user(self, metadata=None):
        super().delete_infra_metadata(name=metadata["params"]["user_id"])

        params = {
            "user_id": self.args.elasticache_user_id,
            "user_name": self.args.elasticache_user_name,
            "access_string": self.args.elasticache_access_string
        }

        super().add_infra_resource("aws_elasticache_user", metadata["params"]["user_id"], params)

    def create_user_group(self, metadata=None):
        super().delete_infra_metadata(name=self.args.name)

        params = {
            "user_group_id": self.args.name,
            "users": self.comma_separated_param_to_list(self.args.elasticache_users)
        }

        super().add_infra_resource("aws_elasticache_user_group", self.args.name, params)

    def comma_separated_param_to_list(self, param):
        return param.replace(" ","").split(",") if param else []
