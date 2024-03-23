from flask import Flask
import boto3
from flask import request
from AudioProcess import convert_audio

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.get_json()
    file_name = convert_audio(file)
    s3 = boto3.client('s3')
    bucket_name = 'hackathonrecordings'

    # Upload the file to S3
    s3.put_object(Body=file, Bucket=bucket_name, Key=file_name)

    return 'File uploaded successfully'