__copyright__ = "Copyright 2023, Kinect Consulting"
__license__ = "Commercial"

import json
import os
import sys
import datetime
import time
import fnmatch
import urllib.parse
import  boto3

from botocore.compat import six
from s3transfer.exceptions import RetriesExceededError as S3TransferRetriesExceededError
from boto3.s3.transfer import TransferConfig
from s3transfer.manager import TransferConfig as S3TransferConfig
from s3transfer.manager import TransferManager
from boto3.exceptions import RetriesExceededError, S3UploadFailedError
from boto3.s3.transfer import S3Transfer
from botocore.exceptions import ClientError

from data_scripts.kc_logging import Logger


class S3:
    def __init__(self, jobName, credentitalName=None):

        self.jobName = jobName
        self.credentitalName = credentitalName

        ##DECLARATION SECTION
        functionID = sys._getframe().f_code.co_name

        self.logger = Logger(self.jobName)
        self.logger.log("INFO", f"Inside method: {functionID}")

    ## If listing out S3 location that have parquet files
    ## , you should not include the filePrefix in the arguments passed to this method
    def getS3FileList(self, bucketName, s3Path, filePrefix=None):

        ##DECLARATION SECTION
        functionID = sys._getframe().f_code.co_name

        self.logger.log("INFO", f"Inside method: {functionID}")

        try:

            s3FileKey = ""
            s3FileKeyList = []
            kwargs = {"Bucket": bucketName, "Prefix": s3Path}

            if self.credentitalName is not None:
                session = boto3.session.Session(profile_name=self.credentitalName)
            else:
                session = boto3.session.Session()

            s3Client = session.client("s3")

            while True:
                response = s3Client.list_objects_v2(**kwargs)
                for obj in response["Contents"]:
                    # exclude directories/folder from results. Remove this if folders are to be removed too
                    if "." in obj["Key"]:
                        s3FileKey = obj["Key"]
                        file = s3FileKey.split("/")[-1]
                        if filePrefix is not None:
                            ## Filter on desired File Prefix wild card match with the actual file
                            if fnmatch.fnmatch(file, filePrefix):
                                s3FileKeyList.append(s3FileKey)
                        else:
                            s3FileKeyList.append(s3FileKey)

                # The S3 API is paginated, returning up to 1000 keys at a time.
                # Pass the continuation token into the next response, until we
                # reach the final page (when this field is missing).
                try:
                    kwargs["ContinuationToken"] = response["NextContinuationToken"]
                except KeyError:
                    break

            return s3FileKeyList

        except ClientError as e:
            msg = e.args
            exceptionMessage = f"Exception Occurred Inside this method {functionID} --> Here is the exception Message {msg}"
            self.logger.log("ERROR", exceptionMessage)
            raise Exception(exceptionMessage)

        except Exception as e:
            msg = e.args
            exceptionMessage = f"Exception Occurred Inside this method {functionID} --> Here is the exception Message {msg}"
            self.logger.log("ERROR", exceptionMessage)
            raise Exception(exceptionMessage)

    def getS3KeyInfo(self, bucketName, s3Path, filePrefix=None):

        ##DECLARATION SECTION
        functionID = sys._getframe().f_code.co_name

        self.logger.log("INFO", f"Inside method: {functionID}")

        try:

            fileKey = []
            fileName = []
            fileTimestamp = []
            fileSize = []
            s3KeyInfo = {}
            kwargs = {"Bucket": bucketName, "Prefix": s3Path}

            if self.credentitalName is not None:
                session = boto3.session.Session(profile_name=self.credentitalName)
            else:
                session = boto3.session.Session()

            s3Client = session.client("s3")

            while True:
                response = s3Client.list_objects_v2(**kwargs)
                for obj in response["Contents"]:
                    # exclude directories/folder from results. Remove this if folders are to be removed too
                    if "." in obj["Key"]:
                        s3FileKey = obj["Key"]
                        file = s3FileKey.split("/")[-1]
                        if filePrefix is not None:
                            ## Filter on desired File Prefix wild card match with the actual file
                            if fnmatch.fnmatch(file, filePrefix):
                                fileKey.append(s3FileKey)
                                fileName.append(file)
                                fileTimestamp.append(obj["LastModified"].timestamp())
                                fileSize.append(obj["Size"])
                        else:
                            fileKey.append(s3FileKey)
                            fileName.append(file)
                            fileTimestamp.append(obj["LastModified"].timestamp())
                            fileSize.append(obj["Size"])

                # The S3 API is paginated, returning up to 1000 keys at a time.
                # Pass the continuation token into the next response, until we
                # reach the final page (when this field is missing).
                try:
                    kwargs["ContinuationToken"] = response["NextContinuationToken"]
                except KeyError:
                    break

            s3KeyInfo = {
                "fileKey": fileKey,
                "fileName": fileName,
                "timestamp": fileTimestamp,
                "fileSize": fileSize,
            }

            return s3KeyInfo

        except ClientError as e:
            msg = e.args
            exceptionMessage = f"Exception Occurred Inside this method {functionID} --> Here is the exception Message {msg}"
            self.logger.log("ERROR", exceptionMessage)
            raise Exception(exceptionMessage)

        except Exception as e:
            msg = e.args
            exceptionMessage = f"Exception Occurred Inside this method {functionID} --> Here is the exception Message {msg}"
            self.logger.log("ERROR", exceptionMessage)
            raise Exception(exceptionMessage)

    def s3_bucket_exists(self, bucket_name):

        ##DECLARATION SECTION
        functionID = sys._getframe().f_code.co_name

        self.logger.log("INFO", f"Inside method: {functionID}")
        try:

            if self.credentitalName is not None:
                session = boto3.session.Session(profile_name=self.credentitalName)
            else:
                session = boto3.session.Session()

            s3_client = session.resource("s3")            
            if s3_client.Bucket(bucket_name).creation_date is not None:
                return True
            else:
                return False

        except Exception as e:
            msg = e.args
            exceptionMessage = f"Exception Occurred Inside this method {functionID} --> Here is the exception Message {msg}"
            self.logger.log("ERROR", exceptionMessage)
            raise Exception(exceptionMessage)

    def s3PrefixExists(self, bucketName, s3Path):

        ##DECLARATION SECTION
        functionID = sys._getframe().f_code.co_name
        isExists = False

        self.logger.log("INFO", f"Inside method: {functionID}")

        try:

            kwargs = {"Bucket": bucketName, "Prefix": s3Path}

            if self.credentitalName is not None:
                session = boto3.session.Session(profile_name=self.credentitalName)
            else:
                session = boto3.session.Session()

            s3Client = session.client("s3")
            response = s3Client.list_objects_v2(**kwargs)
            ## Evaluate the KeyCount property to see if the count > 0, which means that the S3 Prefix location exists.
            if response["KeyCount"] > 0:
                isExists = True

            return isExists

        except ClientError as e:
            msg = e.args
            exceptionMessage = f"Exception Occurred Inside this method {functionID} --> Here is the exception Message {msg}"
            self.logger.log("ERROR", exceptionMessage)
            raise Exception(exceptionMessage)

        except Exception as e:
            msg = e.args
            exceptionMessage = f"Exception Occurred Inside this method {functionID} --> Here is the exception Message {msg}"
            self.logger.log("ERROR", exceptionMessage)
            raise Exception(exceptionMessage)

    def copyFile(self, fromBucket, toBucket, fromPath, toPath):

        ##DECLARATION SECTION
        functionID = sys._getframe().f_code.co_name

        self.logger.log("INFO", f"Inside method: {functionID}")

        try:

            if self.credentitalName is not None:
                session = boto3.session.Session(profile_name=self.credentitalName)
            else:
                session = boto3.session.Session()

            s3Client = session.client("s3")
            copySource = {"Bucket": fromBucket, "Key": fromPath}
            s3Client.copy(copySource, toBucket, toPath)

        except ClientError as e:
            msg = e.args
            exceptionMessage = f"Exception Occurred Inside this method {functionID} --> Here is the exception Message {msg}"
            self.logger.log("ERROR", exceptionMessage)
            raise Exception(exceptionMessage)

        except Exception as e:
            msg = e.args
            exceptionMessage = f"Exception Occurred Inside this method {functionID} --> Here is the exception Message {msg}"
            self.logger.log("ERROR", exceptionMessage)
            raise Exception(exceptionMessage)

    def archiveS3Files(self, fromBucket, toBucket, toPath, sourceFileList):

        ##DECLARATION SECTION
        functionID = sys._getframe().f_code.co_name

        self.logger.log("INFO", f"Inside method: {functionID}")

        try:

            if self.credentitalName is not None:
                session = boto3.session.Session(profile_name=self.credentitalName)
            else:
                session = boto3.session.Session()

            s3Client = session.client("s3")

            if len(sourceFileList) > 0:
                for fileKey in sourceFileList:
                    fromFileKey = fileKey
                    fileName = fileKey.split("/")[-1]
                    copyToLocation = f"{toPath}{fileName}"
                    copySource = {"Bucket": fromBucket, "Key": fromFileKey}
                    s3Client.copy(copySource, toBucket, copyToLocation)

        except ClientError as e:
            msg = e.args
            exceptionMessage = f"Exception Occurred Inside this method {functionID} --> Here is the exception Message {msg}"
            self.logger.log("ERROR", exceptionMessage)
            raise Exception(exceptionMessage)

        except Exception as e:
            msg = e.args
            exceptionMessage = f"Exception Occurred Inside this method {functionID} --> Here is the exception Message {msg}"
            self.logger.log("ERROR", exceptionMessage)
            raise Exception(exceptionMessage)

    def uploadMultipartS3Files(self, toBucket, toPath, sourceFileList, chunkSize=8):

        ##DECLARATION SECTION
        functionID = sys._getframe().f_code.co_name

        self.logger.log("INFO", f"Inside method: {functionID}")

        KB = 1024
        MB = KB * KB

        try:

            if self.credentitalName is not None:
                session = boto3.session.Session(profile_name=self.credentitalName)
            else:
                session = boto3.session.Session()

            s3Client = session.client("s3")
            config = TransferConfig(
                multipart_threshold=8 * MB,
                use_threads=False,
                multipart_chunksize=8 * MB,
            )
            transfer = S3Transfer(s3Client, config)

            if len(sourceFileList) > 0:
                for fileKey in sourceFileList:
                    fromFileKey = fileKey
                    fileName = fileKey.split("/")[-1]
                    copyToLocation = f"{toPath}{fileName}"

                    transfer.upload_file(fromFileKey, toBucket, copyToLocation)

        except ClientError as e:
            msg = e.args
            exceptionMessage = f"Exception Occurred Inside this method {functionID} --> Here is the exception Message {msg}"
            self.logger.log("ERROR", exceptionMessage)
            raise Exception(exceptionMessage)

        except Exception as e:
            msg = e.args
            exceptionMessage = f"Exception Occurred Inside this method {functionID} --> Here is the exception Message {msg}"
            self.logger.log("ERROR", exceptionMessage)
            raise Exception(exceptionMessage)

    def deleteEODPartition(self, s3Bucket, folderPrefix):

        ##DECLARATION SECTION
        functionID = sys._getframe().f_code.co_name

        self.logger.log("INFO", f"Inside method: {functionID}")

        try:

            kwargs = {"Bucket": s3Bucket, "Prefix": folderPrefix}

            if self.credentitalName is not None:
                session = boto3.session.Session(profile_name=self.credentitalName)
            else:
                session = boto3.session.Session()

            s3Client = session.client("s3")
            s3Objects = s3Client.list_objects_v2(**kwargs)
            if "Contents" in s3Objects:
                for file in s3Objects["Contents"]:
                    fileKey = file["Key"]
                    fileSize = file["Size"]

                    if fileSize > 0:
                        fileName = fileKey.split("/")[-1]

                        self.logger.log("INFO", "Deleting file {}".format(fileName))

                        deleteResponse = s3Client.delete_object(
                            Bucket=s3Bucket, Key=fileKey
                        )
                    
                    self.logger.log("INFO", deleteResponse)

        except ClientError as e:
            msg = e.args
            exceptionMessage = f"Exception Occurred Inside this method {functionID} --> Here is the exception Message {msg}"
            self.logger.log("ERROR", exceptionMessage)
            raise Exception(exceptionMessage)

        except Exception as e:
            msg = e.args
            exceptionMessage = f"Exception Occurred Inside this method {functionID} --> Here is the exception Message {msg}"
            self.logger.log("ERROR", exceptionMessage)
            raise Exception(exceptionMessage)

    def deleteFiles(self, s3Bucket, s3Prefix):
        functionID = sys._getframe().f_code.co_name

        try:
            if self.credentitalName is not None:
                session = boto3.session.Session(profile_name=self.credentitalName)
            else:
                session = boto3.session.Session()

            s3Client = session.resource("s3")
            bucket = s3Client.Bucket(s3Bucket)
            bucket.objects.filter(Prefix=s3Prefix).delete()

        except ClientError as e:
            msg = e.args
            exceptionMessage = f"Exception Occurred Inside this method {functionID} --> Here is the exception Message {msg}"
            self.logger.log("ERROR", exceptionMessage)
            raise Exception(exceptionMessage)

        except Exception as e:
            msg = e.args
            exceptionMessage = f"Exception Occurred Inside this method {functionID} --> Here is the exception Message {msg}"
            self.logger.log("ERROR", exceptionMessage)
            raise Exception(exceptionMessage)
