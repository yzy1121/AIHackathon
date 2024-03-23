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

def convert_txt(file_name):
    # Load the json data
    with open(file_name, 'r') as file:
        json_data = json.load(file)

    # Extract the transcription text
    transcription = json_data['results']['transcripts'][0]['transcript']

    # Save the transcription to a text file
    with open('transcription.txt', 'w') as text_file:
        text_file.write(transcription)

    print("Transcription text has been saved to 'transcription.txt'")
        

# snippet-start:[python.example_code.comprehend.Usage_DetectApis]
def start_analysis(file_name):
    print("-" * 88)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    
    convert_txt(file_name)

    senti_analysis = SentimentAnalysis(boto3.client("comprehend"))
    with open("transcription.txt") as sample_file:
        sample_text = sample_file.read()

    lang_code = "en"

    print("Detecting sentiment.")
    sentiment = senti_analysis.detect_sentiment(sample_text, lang_code)
    print(f"Sentiment: {sentiment['Sentiment']}")
    print("SentimentScore:")
    pprint(sentiment["SentimentScore"])

    print("-" * 88)


# snippet-end:[python.example_code.comprehend.Usage_DetectApis]


if __name__ == "__main__":
    start_analysis('asrOutput.json')