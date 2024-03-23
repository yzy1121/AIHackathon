import logging
import time
import boto3
from botocore.exceptions import ClientError
import os
import urllib.request


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

def transcribe_file(job_name, file_uri, transcribe_client):
    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": file_uri},
        MediaFormat="wav",
        LanguageCode="en-US",
        OutputBucketName="hackathontranscriptions",
        Settings={
        'ShowSpeakerLabels': True,
        'MaxSpeakerLabels': 10
        }
    )

    max_tries = 60
    while max_tries > 0:
        max_tries -= 1
        job = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        job_status = job["TranscriptionJob"]["TranscriptionJobStatus"]
        if job_status in ["COMPLETED", "FAILED"]:
            print(f"Job {job_name} is {job_status}.")
            if job_status == "COMPLETED":
                print(
                    f"Download the transcript from\n"
                    f"\t{job['TranscriptionJob']['Transcript']['TranscriptFileUri']}."
                )
            break
        else:
            print(f"Waiting for {job_name}. Current status is {job_status}.")
        time.sleep(10)



def main():
    # upload file to s3
    file_name = "test0.wav"
    bucket = "hackathonrecordings"
    upload_file(file_name, bucket)

    transcribe_client = boto3.client("transcribe")
    file_uri = "s3://hackathonrecordings/test0.wav"

    transcribe_file("Hackathon-jobtest1", file_uri, transcribe_client)


if __name__ == "__main__":
    main()