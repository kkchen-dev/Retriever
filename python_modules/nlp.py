import os
import pathlib
# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

class NLP:
    def __init__(self):
        # Sets environmental varable
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = f"{pathlib.Path(__file__).parent.resolve()}/google_cloud_api.json"
        # Instantiates a client
        self.client = language.LanguageServiceClient()

    def analyze(self, text):
        document = types.Document(
            content=text,
            type=enums.Document.Type.PLAIN_TEXT,
            language="en-US")
        sentiment = self.client.analyze_sentiment(document=document).document_sentiment

        return {"score": sentiment.score, "magnitude": sentiment.magnitude}


if __name__ == "__main__":
    # The text to analyze
    text = "Good luck!"
    nlp = NLP()
    sentiment = nlp.analyze(text)
    print(sentiment["score"], sentiment["magnitude"])