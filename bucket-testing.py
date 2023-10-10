import boto3
import os

ACCESS_KEY = os.environ['ACCESS_KEY']
SECRET_KEY = os.environ['SECRET_KEY']

s3 = boto3.resource('s3')
bucket = 'be-sharebnb-listing-photos'

for bucket in s3.buckets.all():
    print(bucket.name)

s3 = boto3.client(
    's3',
    'us-west-1',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)


def upload_file(file_name, bucket, object_name):
    """Uploads file to AWS bucket."""


upload_file('house.jpg', bucket, s3)
