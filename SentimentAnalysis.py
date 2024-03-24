from enum import Enum
import logging
from pprint import pprint
import boto3
from botocore.exceptions import ClientError
import json

logger = logging.getLogger(__name__)

class SentimentAnalysis:
    """Encapsulates Comprehend detection functions."""

    def __init__(self, comprehend_client):
        """
        :param comprehend_client: A Boto3 Comprehend client.
        """
        self.comprehend_client = comprehend_client

    # snippet-start:[python.example_code.comprehend.DetectSentiment]
    def detect_sentiment(self, text, language_code):
        """
        Detects the overall sentiment expressed in a document. Sentiment can
        be positive, negative, neutral, or a mixture.

        :param text: The document to inspect.
        :param language_code: The language of the document.
        :return: The sentiments along with their confidence scores.
        """
        try:
            response = self.comprehend_client.detect_sentiment(
                Text=text, LanguageCode=language_code
            )
            logger.info("Detected primary sentiment %s.", response["Sentiment"])
        except ClientError:
            logger.exception("Couldn't detect sentiment.")
            raise
        else:
            return response

    # snippet-end:[python.example_code.comprehend.DetectSentiment]

def convert_txt(file):
    # Load the json data
    json_data = file.read()
    # Extract the transcription text
    transcription = json_data['results']['transcripts'][0]['transcript']

    # Save the transcription to a text file in s3 bucket
    s3 = boto3.resource('s3')
    bucket_name = 'hackathontranscripts'
    s3.Object(bucket_name, f"{json_data['jobName']}.txt").put(Body=transcription)

    # delete the json file from s3
    bucket = s3.Bucket(bucket_name)
    for obj in bucket.objects.all():
        if obj.key == file:
            obj.delete()
            print(f"Deleted {obj.key} from {bucket_name}.")

    print("Transcription text has been saved to 'transcription.txt'")
    return f'{json_data['jobName']}.txt'
        

# snippet-start:[python.example_code.comprehend.Usage_DetectApis]
def start_analysis():
    print("-" * 88)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    senti_analysis = SentimentAnalysis(boto3.client("comprehend"))
    # convert every file in the s3 bucket to txt
    s3 = boto3.resource('s3')
    bucket_name = 'hackathontranscripts'
    bucket = s3.Bucket(bucket_name)
    text_files = []

    for obj in bucket.objects.all():
        if obj.key.endswith('.json'):
            text_files.append(obj.key)

    for file in text_files:
        for obj in bucket.objects.all():
            if obj.key == file:
                file_name = convert_txt(obj)
                
                # load the converted text file from s3
                transcribe_file = s3.Object(bucket_name, file_name)
                transcribe_text = transcribe_file.read()

                lang_code = "en"

                print("Detecting sentiment.")
                sentiment = senti_analysis.detect_sentiment(transcribe_text, lang_code)
                print(f"Sentiment: {sentiment['Sentiment']}")
                print("SentimentScore:")
                pprint(sentiment["SentimentScore"])

                print("-" * 88)

                # delete the text file from s3
                obj.delete()
                print(f"Deleted {obj.key} from {bucket_name}.")

# snippet-end:[python.example_code.comprehend.Usage_DetectApis]


if __name__ == "__main__":
    start_analysis()