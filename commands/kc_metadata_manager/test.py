__author__ = "Igor Royzis"
__copyright__ = "Copyright 2020, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import logging

from commands.kc_metadata_manager.aws_metadata import Metadata

class Test(Metadata):

    logger = logging.getLogger(__name__)

    def __init__(self, args):
        print("")
        self.args = args
        self.logger.info("BEFORE super().__init__(args)")
        self.run()
        print("")
        self.logger.info("AFTER super().__init__(args)")
        super().__init__(args)


    def run(self):
        for attr in ["env", "aws_profile", "region_name"]:
            if hasattr(self, attr):
                self.logger.info(f"  self.{attr}: {getattr(self, attr)}")
            else:
                self.logger.info(f"  self.{attr}:")

            if hasattr(self.args, attr):
                self.logger.info(f"  self.args.{attr}: {getattr(self.args, attr)}")
            else:
                self.logger.info(f"  self.args.{attr}:")
