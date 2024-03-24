from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import ClientError
import base64
import os
import tempfile
import logging
from werkzeug.utils import secure_filename
from AudioProcess import convert_json_to_m4a

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

# @app.route('/upload', methods=['POST'])
# def upload():
#     # Check for the correct content type
#     if request.headers.get('Content-Type') == 'application/json':
#         data = request.get_json()

#         # Validate the JSON data
#         if not data or 'content' not in data:
#             return jsonify({'error': 'Invalid or missing audio data'}), 400

#         # Convert the JSON data to an M4A file
#         file_name = convert_json_to_m4a(data)
#         print(f"File name: {file_name}")
#         if not file_name:
#             return jsonify({'error': 'Failed to convert data to audio file'}), 500

#         bucket_name = 'hackathonrecordings'
#         uploaded = upload_file_to_s3(file_name, bucket_name)

#         # Cleanup: Remove the temporary file
#         try:
#             os.remove(file_name)
#         except OSError as e:
#             print(f"Error deleting temporary file {file_name}: {e}")

#         # Check the result of the upload
#         if uploaded:
#             return jsonify({'message': 'File uploaded successfully'}), 200
#         else:
#             return jsonify({'error': 'Failed to upload file to S3'}), 500
#     else:
#         return jsonify({'error': 'Unsupported Media Type'}), 415
# Setup basic logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    if request.headers.get('Content-Type') == 'application/json':
        data = request.get_json()
        # print(data)
        if not data or 'content' not in data:
            return jsonify({'error': 'Invalid or missing audio data'}), 400

        # Process the audio data and obtain a file path
        file_name = convert_json_to_m4a(data)

        if not file_name:
            logging.error("No file name returned from conversion")
            return jsonify({'error': 'Failed to convert data to audio file'}), 500

        # The file_name must be a string path, here we can log it to ensure it is correct
        if not isinstance(file_name, str):
            logging.error(f"Invalid file_name type: {type(file_name)}. Expected a file path as a string.")
            return jsonify({'error': 'Internal server error'}), 500

        # Secure the file name before using it
        secure_file_name = secure_filename(file_name)

        bucket_name = 'hackathonrecordings'
        uploaded = upload_file_to_s3(secure_file_name, bucket_name)

        # Check the result of the upload
        if uploaded:
            return jsonify({'message': 'File uploaded successfully'}), 200
        else:
            return jsonify({'error': 'Failed to upload file to S3'}), 500
    else:
        return jsonify({'error': 'Unsupported Media Type'}), 415

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
