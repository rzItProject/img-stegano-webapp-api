import boto3
from botocore.exceptions import BotoCoreError, NoCredentialsError, PartialCredentialsError

class S3UploadError(Exception):
    """Raised when there's an error uploading to S3"""


class S3Repository():
    def __init__(self, access_key: str, secret_key: str, endpoint_url: str):
        self.s3 = boto3.client(
            service_name='s3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            endpoint_url=endpoint_url
        )

    def list_buckets(self):
        return [bucket.name for bucket in self.s3.buckets.all()]

    def upload_file(self, bucket: str, file, filename: str):
        try:
            self.s3.upload_fileobj(file, bucket, filename)
        except NoCredentialsError:
            raise S3UploadError("Credentials not available")
        except PartialCredentialsError:
            raise S3UploadError("Incomplete credentials provided")
        except BotoCoreError as e:
            raise S3UploadError(f"An error occurred: {str(e)}")

    def download_file(self, bucket_name: str, key: str, output_path: str):
        self.s3.Bucket(bucket_name).download_file(Key=key, Filename=output_path)
