import logging
import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY = os.environ['ACCESS_KEY']
AWS_SECRET_KEY = os.environ['SECRET_KEY']

bucket = 'be-sharebnb-listing-photos'


def upload_file(file_name, bucket, object_name=None):
    """Uploads file to AWS bucket."""
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client(
        's3',
        'us-west-1',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
    )
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


s3 = boto3.client('s3')
with open("house.jpg", 'rb') as f:
    s3.upload_fileobj(f, bucket, "house.jpg")
