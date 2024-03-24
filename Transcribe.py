import logging
import time
import boto3
from botocore.exceptions import ClientError
import os


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
                # delete the audio file from s3
                s3 = boto3.resource('s3')
                bucket_name = 'hackathonrecordings'
                bucket = s3.Bucket(bucket_name)
                for obj in bucket.objects.all():
                    if obj.key == file_uri.split('/')[-1]:
                        obj.delete()
                        print(f"Deleted {obj.key} from {bucket_name}.")
            break
        else:
            print(f"Waiting for {job_name}. Current status is {job_status}.")
        time.sleep(10)



def transcribe():
    transcribe_client = boto3.client("transcribe")
    # load the audio files from s3
    s3 = boto3.resource('s3')
    bucket_name = 'hackathonrecordings'
    bucket = s3.Bucket(bucket_name)
    audio_files = []

    for obj in bucket.objects.all():
        if obj.key.endswith('.wav'):
            audio_files.append(obj.key)

    # Use the audio_files list to process each audio file
    for file in audio_files:
        file_uri = f"s3://{bucket_name}/{file}"
        job_name = f"job-{file.split('.')[0]}"
        transcribe_file(job_name, file_uri, transcribe_client)

if __name__ == "__main__":
    transcribe()