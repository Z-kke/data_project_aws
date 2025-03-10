import json
import os
import uuid

import boto3
import requests


class DataIngestor:
    def __init__(self, api_url, db_table="DataIngestionTable"):
        self.api_url = api_url
        self.db_table = db_table

        # Initialize a DynamoDB resource using boto3.
        self.dynamodb = boto3.resource("dynamodb", region_name="eu-north-1")
        self.table = self.dynamodb.Table(self.db_table)

    def fetch_data(self):
        """Fetch data from the API."""
        response = requests.get(self.api_url)
        response.raise_for_status()  # Raises HTTPError for bad responses.
        return response.json()

    def process_data(self, data):
        """Process the API data (modify as needed)."""
        # For now, we simply return the data as-is.
        return data

    def store_data(self, data):
        """Store processed data in DynamoDB."""
        # Create an item with a unique id.
        item = {"id": str(uuid.uuid4()), "data": data}
        # Write the item into the DynamoDB table.
        self.table.put_item(Item=item)
        return item


def lambda_handler(event, context):
    api_url = os.environ.get("API_URL", "https://opentdb.com/api.php?amount=10")
    db_table = os.environ.get("DB_TABLE", "DataIngestionTable")

    ingestor = DataIngestor(api_url, db_table)
    try:
        raw_data = ingestor.fetch_data()
        processed_data = ingestor.process_data(raw_data)
        stored_item = ingestor.store_data(processed_data)
        return {
            "statusCode": 200,
            "body": json.dumps(
                {"message": "Data processed and stored", "stored_item": stored_item}
            ),
        }
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
