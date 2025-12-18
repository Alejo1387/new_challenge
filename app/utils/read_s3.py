from app.core.s3 import get_s3_client

def read_file(key):
    s3 = get_s3_client()

    response = s3.get_object(
        Bucket="my-test-bucket",
        Key=key
    )

    return response['Body'].read()