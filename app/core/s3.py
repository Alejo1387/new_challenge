import boto3

from moto import mock_aws

mock = mock_aws()

def get_s3_client():
    mock.start()

    s3 = boto3.client(
        "s3",
        region_name="us-east-1",
        aws_access_key_id="fake",
        aws_secret_access_key="fake"
    )

    buckets = s3.list_buckets()["Buckets"]
    if not any(b["Name"] == "my-test-bucket" for b in buckets):
        s3.create_bucket(Bucket="my-test-bucket")

    return s3