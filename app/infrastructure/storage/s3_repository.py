import boto3

class S3Repository():
    def __init__(self, access_key: str, secret_key: str, endpoint_url: str):
        self.s3 = boto3.resource(
            service_name='s3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            endpoint_url=endpoint_url
        )

    def list_buckets(self):
        return [bucket.name for bucket in self.s3.buckets.all()]

    def upload_file(self, bucket: str, file, filename: str):
        self.s3.upload_fileobj(file, bucket, filename)

    def download_file(self, bucket_name: str, key: str, output_path: str):
        self.s3.Bucket(bucket_name).download_file(Key=key, Filename=output_path)
