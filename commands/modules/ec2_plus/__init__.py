__author__ = "Igor Royzis"
__copyright__ = "Copyright 2022, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

from commands.kc_metadata_manager.aws_metadata import Metadata

class ModuleMetadata(Metadata):

    def __init__(self, args):
        super().__init__(args)


    def create(self, metadata=None):
        pass
        