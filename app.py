from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import ClientError
import base64
import os
import tempfile
import logging
from werkzeug.utils import secure_filename
from AudioProcess import convert_json_to_m4a
from Transcribe import transcribe
from FileReceiver import upload
from SentimentAnalysis import start_analysis
app = Flask(__name__)

@app.route('/', methods=['POST'])
def execution():
    # keep processing the incoming json files
    upload()

    # while the bucket of audio is not empty, keep executing transcribe
    s3 = boto3.resource('s3')
    bucket_name = 'hackathonrecordings'
    bucket_rec = s3.Bucket(bucket_name)
    objects_iterator = iter(bucket_rec.objects.all())
    while True:
        try:
            # Attempt to get the next object
            next(objects_iterator)
            transcribe()
        except StopIteration:
            # No more objects, exit the loop
            print("No more objects in the bucket.")
            break
    
    # while the bucket of transcriptions is not empty, keep executing sentiment analysis
    s3 = boto3.resource('s3')
    bucket_name = 'hackathontranscriptions'
    bucket_trans = s3.Bucket(bucket_name)
    objects_iterator = iter(bucket_trans.objects.all())
    while True:
        try:
            # Attempt to get the next object
            next(objects_iterator)
            start_analysis()
        except StopIteration:
            # No more objects, exit the loop
            print("No more objects in the bucket.")
            break
    return

if __name__ == '__main__':
    app.run(debug=True)