__author__ = "Igor Royzis"
__license__ = "MIT"


from commands.kc_metadata_manager.aws_metadata import Metadata

class ModuleMetadata(Metadata):

    def __init__(self, args):
        super().__init__(args)


    def create(self, metadata=None):
        pass
        