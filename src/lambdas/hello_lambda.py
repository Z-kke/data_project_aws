import json
import os

import requests


class DataIngestor:
    def __init__(self, api_url):
        self.api_url = api_url

    def fetch_data(self):
        """Fetch data from the API."""
        response = requests.get(self.api_url)
        response.raise_for_status()  # Raise error if the API call fails
        return response.json()

    def process_data(self, data):
        """Process the API data."""
        return data


def lambda_handler(event, context):
    api_url = os.environ.get("API_URL", "https://opentdb.com/api.php?amount=10")
    ingestor = DataIngestor(api_url)
    try:
        raw_data = ingestor.fetch_data()
        processed_data = ingestor.process_data(raw_data)
        return {"statusCode": 200, "body": json.dumps(processed_data)}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
