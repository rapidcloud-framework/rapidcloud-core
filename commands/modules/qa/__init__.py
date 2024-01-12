__author__ = "iroyzis@kinect-consulting.com"

from commands.modules.qa.integration_tests import IntegrationTests
from commands.kc_metadata_manager.aws_metadata import Metadata

class ModuleMetadata(Metadata):

    def __init__(self, args):
        super().__init__(args)
        self.args = args


    def run_cli_tests(self, metadata=None):
        IntegrationTests(self).run_tests()
