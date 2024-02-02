__author__ = "Igor Royzis"
__license__ = "MIT"


from commands.kc_metadata_manager.aws_metadata import Metadata
from commands.modules import exec_module

class ModuleMetadata(Metadata):

    def __init__(self, args):
        super().__init__(args)
        self.args = args


    def create_bucket(self, metadata=None):
        self.add_aws_resource("s3_bucket", self.args.name)
        if self.args.s3_enable_trend == "true":
            self.enable_trend(metadata)


    def enable_trend(self, metadata=None):
        if self.args.s3_enable_trend == "true":
            setattr(self.args, "stack_type", "storage")
            setattr(self.args, "bucket", self.args.name)
            exec_module(self.args, "trendmicro", "filestorage_create_stack")


    def ls(self, metadata=None):
        pass
