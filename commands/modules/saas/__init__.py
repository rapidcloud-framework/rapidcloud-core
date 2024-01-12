__author__ = "iroyzis@kinect-consulting.com"

import argparse
import json
import logging
from commands.kc_metadata_manager.aws_metadata import Metadata
from commands.cli_worker.license_worker import LicenseWorker
from licensing import saas

class ModuleMetadata(Metadata):

    logger = logging.getLogger(__name__)

    def __init__(self, args):
        super().__init__(args)
        self.args = args
        self.lic_worker = LicenseWorker(self.args)

    def exec(self, metadata=None):
        args = {}
        for arg in ["action","domain","email","app_env","output_key","cmd"]:
            args[arg] = metadata.get(arg)
        resp = saas.exec(args)
        setattr(self.args, "response", resp)
        return resp