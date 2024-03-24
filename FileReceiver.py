from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import ClientError
import base64
import os
import tempfile
import logging

app = Flask(__name__)

# Placeholder for converting JSON with base64 audio data to a file
def convert_audio(audio_data):
    # Decode the base64 audio content to binary
    audio_content = base64.b64decode(audio_data['content'])

    # Create a temporary file to save the audio
    temp_fd, temp_path = tempfile.mkstemp()
    with os.fdopen(temp_fd, 'wb') as tmp:
        # Write the decoded audio data to the file
        tmp.write(audio_content)
    
    return temp_path

def upload_file_to_s3(file_name, bucket, object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

@app.route('/upload', methods=['POST'])
def upload():
    if request.headers.get('Content-Type') == 'application/json':
        file = request.get_json()
        if not file or 'content' not in file:
            return jsonify({'error': 'Invalid or missing audio data'}), 400

        file_name = convert_audio(file)
        bucket_name = 'hackathonrecordings'

        # Upload the file to S3 and clean up the temporary file
        if upload_file_to_s3(file_name, bucket_name):
            os.remove(file_name)  # Cleanup temporary file
            return jsonify({'message': 'File uploaded successfully'}), 200
        else:
            os.remove(file_name)  # Cleanup temporary file
            return jsonify({'error': 'Failed to upload file to S3'}), 500
    else:
        return jsonify({'error': 'Unsupported Media Type'}), 415

if __name__ == '__main__':
    app.run(debug=True)
