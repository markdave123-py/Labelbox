import boto3
from app.config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, S3_BUCKET_NAME
import uuid
import re
import time

def upload_file_to_s3(file_bytes, file_content_type, filename):
    s3 = boto3.client('s3',
                      region_name=AWS_REGION,
                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    # Generate a unique filename
    filename = f"{uuid.uuid4()}.png"
    s3.put_object(
        Bucket=S3_BUCKET_NAME,
        Key=filename,
        Body=file_bytes,
        ContentType=file_content_type,
        ContentDisposition="inline"
    )

    # Construct the public URL
    url = f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{filename}"
    return url

def generate_clean_filename(original_filename: str) -> str:
    # Extract filename and extension
    name, ext = original_filename.rsplit(".", 1)
    cleaned_name = re.sub(r"[^a-zA-Z0-9_-]", "", name)
    timestamp = int(time.time())  
    return f"{cleaned_name}-{timestamp}.{ext}"