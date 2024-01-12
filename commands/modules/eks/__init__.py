__author__ = "mlevy@kinect-consulting.com"

from commands.kc_metadata_manager.aws_metadata import Metadata
from commands.kc_metadata_manager.aws_infra import AwsInfra

import pprint
import json
import os
from boto3.dynamodb.conditions import Attr


class ModuleMetadata(Metadata):

    def __init__(self, args):
        super().__init__(args)
        self.args = args
        self.boto3_session = super().get_boto3_session()

    def pp(self, v):
        if 'RAPIDCLOUD_TEST_MODE_AWS_EKS' in os.environ and os.environ.get('RAPIDCLOUD_TEST_MODE_AWS_EKS') == "true":
            print(pprint.pformat(v))

    def load_params(self, module, command, args):
        # we will populate this dict and pass it to the command functions
        params = {}
        try:
            # we're pulling all valus from the args object into a dict
            args_dict = vars(args)

            # we then load the actual args from the module's json
            json_args = self.get_module_json("eks")[module][command]['args']

            # now we'll loop over them all
            for arg in json_args.keys():
                params[arg] = args_dict[f"{module}_{arg}"]
                if arg == 'tags' or arg == 'labels' or arg == 'selectors':
                    # convert string to dict here
                    arg_json = json.loads(args_dict[f"{module}_{arg}"].replace("\\", ""))
                    try:
                        params[arg] = arg_json
                    except Exception as e:
                        print(e)
        except Exception as e:
            print(f"init.py error: {e}")
        return params

    def load_fargate_profile_selector_labels(self, module, command, args):
        fargate_selectors = [
            "namespace_1_labels", "namespace_2_labels", "namespace_3_labels", "namespace_4_labels", "namespace_5_labels"
        ]
        # we will populate this dict and pass it to the command functions
        params = {}
        try:
            args_dict = vars(args)

            # we then load the actual args from the module's json
            json_args = self.get_module_json("eks")[module][command]['args']

            # now we'll loop over them all
            for arg in fargate_selectors:
                params[arg] = args_dict[f"{module}_{arg}"]
                # convert string to dict here
                arg_json = json.loads(args_dict[f"{module}_{arg}"].replace("\\", ""))
                try:
                    params[arg] = arg_json
                except Exception as e:
                    print(e)
        except Exception as e:
            print(f"fargate init.py error: {e}")
        return params

    def create_cluster(self, metadata=None):
        super().delete_infra_metadata(name=self.args.cluster_name)
        params = self.load_params('eks', 'create_cluster', self.args)
        resource_name = self.args.cluster_name
        resource_type = "aws_eks_cluster"
        super().add_aws_resource(resource_type, resource_name, params)

    def check_for_aws_auth_refresh(self, cluster_name):
        # check if a metadata item exists for aws_auth_command and this cluster
        aws_auth_md = {}
        filters = (Attr('command').eq('manage_aws_auth') & Attr('params.cluster_name').eq(cluster_name))

        aws_auth_result = super().get_all_resources(extra_filters=filters)

        # if we get a result, call the aws_auth manage function
        if len(aws_auth_result) > 0:
            aws_auth_md['profile'] = aws_auth_result[0]['profile']
            aws_auth_md['phase'] = aws_auth_result[0]['phase']
            aws_auth_md['cmd_id'] = aws_auth_result[0]['cmd_id']
            aws_auth_md['command'] = aws_auth_result[0]['command']
            aws_auth_md['fqn'] = aws_auth_result[0]['fqn']
            aws_auth_md['params'] = aws_auth_result[0]['params']
            for k, v in aws_auth_result[0]['params'].items():
                aws_auth_md[f"eks_{k}"] = v
            self.manage_aws_auth(aws_auth_md, True)

    def create_node_group(self, metadata=None):
        super().delete_infra_metadata(name=self.args.node_group_name)
        params = self.load_params('eks', 'create_node_group', self.args)
        resource_name = self.args.node_group_name
        resource_type = "aws_eks_node_group"
        super().add_aws_resource(resource_type, resource_name, params)
        # since aws-auth config map needs to be aware of compute resources
        # we refresh it in this stage
        self.check_for_aws_auth_refresh(self.args.eks_cluster_name)

    def remove_node_group(self, metadata=None):
        AwsInfra(self.args).undo_command()
        self.check_for_aws_auth_refresh(self.args.eks_cluster_name)

    def remove_eks_cluster(self, metadata=None):
        try:
            command_list = []
            filters = Attr('phase').eq('eks') & Attr('params.cluster_name').eq(self.args.eks_cluster_name)
            result = super().get_all_resources(extra_filters=filters)
            for i in result:
                command_list.append(i['command'])
            command_list.remove('create_cluster')
        except Exception as e:
            self.pp(e)

        # if we get a result, call the aws_auth manage function
        if len(command_list) > 0:
            raise Exception(
                f"Validation Failed!, Please make sure you remove and APPLY any dependent module prior to remove this module"
                f"({','.join(command_list)})")
        else:
            AwsInfra(self.args).undo_command()

    def create_fargate_profile(self, metadata=None):
        super().delete_infra_metadata(name=self.args.profile_name)
        params = self.load_params('eks', 'create_fargate_profile', self.args)
        selector_params = self.load_fargate_profile_selector_labels('eks', 'create_fargate_profile', self.args)
        params.update(selector_params)
        resource_name = self.args.profile_name
        resource_type = "aws_eks_fargate_profile"
        super().add_aws_resource(resource_type, resource_name, params)
        # since aws-auth config map needs to be aware of compute resources
        # we refresh it in this stage
        self.check_for_aws_auth_refresh(self.args.eks_cluster_name)

    def remove_fargate_profile(self, metadata=None):
        AwsInfra(self.args).undo_command()
        self.check_for_aws_auth_refresh(self.args.eks_cluster_name)

    def manage_addons(self, metadata=None):
        super().delete_infra_metadata(name=self.args.cluster_name)
        params = self.load_params('eks', 'manage_addons', self.args)
        resource_name = self.args.cluster_name
        resource_type = "aws_eks_addons"
        super().add_aws_resource(resource_type, resource_name, params)

    def manage_extras(self, metadata=None):
        super().delete_infra_metadata(name=self.args.cluster_name)
        params = self.load_params('eks', 'manage_extras', self.args)
        resource_name = self.args.cluster_name
        resource_type = "aws_eks_extras"
        super().add_aws_resource(resource_type, resource_name, params)

    def load_aws_auth_params_from_file(self, module, command, params):
        try:
            for arg in ['map_roles', 'map_users']:
                # load file from file
                if arg in params.keys() and params[arg] != "":
                    try:
                        with open(params[arg], 'r') as f:
                            params[f"{arg}_values"] = json.load(f)
                    # except Exception as e:
                    #     print(f"init.py load from eks_file exception error: {e}")
                    #     with open(params[f"eks_{arg}"], 'r') as f:
                    #         params[f"{arg}_values"] = json.load(f)
                    except Exception as e:
                        print(f"init.py load from eks_file exception error {e}")

                # load from console
                elif f"{arg}_values" in params.keys():
                    try:
                        arg_value = json.loads(params[f"{arg}_values"].replace("\\", ""))
                        params[f"{arg}_values"] = arg_value
                    except Exception as e:
                        print(f"init.py arg values error: {e}")

                elif f"eks_{arg}_values" in params.keys():
                    try:
                        arg_value = json.loads(params[f"eks_{arg}_values"].replace("\\", ""))
                        params[f"eks_{arg}_values"] = arg_value
                    except Exception as e:
                        print(f"init.py eks arg values error: {e}")

        except Exception as e:
            print(f"init.py error: {e}")
        return params

    def load_eks_compute(self, module, command, cluster_name):
        # this function will look up node group and fargate profile names from aws_infra
        # it will then pass those to the jinja template for aws_auth so that we can add
        # the proper iam roles to the cluster
        node_groups = []
        fargate_profiles = []
        filters = (Attr('command').eq('create_node_group')
                   | Attr('command').eq('create_fargate_profile')) & Attr('params.cluster_name').eq(cluster_name)
        aws_infra = super().get_all_resources(extra_filters=filters)
        for i in aws_infra:
            try:
                if i['command'] == 'create_node_group' and i['params']['cluster_name'] == cluster_name:
                    node_groups.append(i['params']['node_group_name'])
                if i['command'] == 'create_fargate_profile' and i['params']['cluster_name'] == cluster_name:
                    fargate_profiles.append(i['params']['profile_name'])
            except Exception as e:
                self.pp(e)
        return node_groups, fargate_profiles

    def manage_aws_auth(self, metadata=None, refresh=False):
        try:
            if refresh:
                self.args.command = metadata['command']
                self.args.cmd_id = metadata['cmd_id']
                self.args.cluster_name = metadata['eks_cluster_name']
                self.args.fqn = metadata['fqn']
                params = metadata['params']
            else:
                raw_params = self.load_params('eks', 'manage_aws_auth', self.args)
                params = self.load_aws_auth_params_from_file('eks', 'manage_aws_auth', raw_params)

            super().delete_infra_metadata(name=self.args.cluster_name)
            node_groups, fargate_profiles = self.load_eks_compute('eks', 'manage_aws_auth', self.args.cluster_name)
            params['node_groups'] = node_groups
            params['fargate_profiles'] = fargate_profiles

            resource_name = self.args.cluster_name
            resource_type = "aws_eks_aws_auth"
            super().add_aws_resource(resource_type, resource_name, params)

        except Exception as e:
            self.pp(e)
