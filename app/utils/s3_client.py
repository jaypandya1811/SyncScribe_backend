from dotenv import load_dotenv, find_dotenv
import boto3
import os

dotenv_path = find_dotenv()

load_dotenv(dotenv_path, override=True)
s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)


BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")