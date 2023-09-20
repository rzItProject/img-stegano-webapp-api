import boto3

# Let's use S3
s3 = boto3.resource(
    service_name='s3',
    aws_access_key_id='zYHXMlSzpZDrNrc8',
    aws_secret_access_key='ft7TvAGY6aTCOo49M0hS7pJEig8rumbiMNeSiyZy',
    endpoint_url='https://s3.tebi.io'
)

def test_boto3_connection():
    try:
        # Print out bucket names
        for bucket in s3.buckets.all():
            print(bucket.name)
    except Exception as e:
        print("Connection Failed:", str(e))
        return False

if __name__ == "__main__":
    success = test_boto3_connection()
    if success:
        print("Boto3 connection successful!")
    else:
        print("Boto3 connection failed!")