from flask import Flask
import boto3
from flask import request
import logging
from AudioProcess import convert_audio
from botocore.exceptions import ClientError
import os

app = Flask(__name__)


def upload_file(file_name, bucket, object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True



@app.route('/upload', methods=['POST'])
def upload():
    file = request.get_json()
    file_name = convert_audio(file)
    bucket_name = 'hackathonrecordings'

    # Upload the file to S3
    upload_file(file_name, bucket_name)

    return 'File uploaded successfully'