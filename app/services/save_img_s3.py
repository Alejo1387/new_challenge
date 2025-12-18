from app.core.s3 import get_s3_client

def upload_qr(file_bytes, file_name):
    s3 = get_s3_client()

    s3.put_object(
        Bucket="my-test-bucket",
        Key=f"img/{file_name}",
        Body=file_bytes
    )

    return f"img/{file_name}"