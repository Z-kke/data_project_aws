import json

from lambdas.hello_lambda import DataIngestor, lambda_handler


def dummy_get(url):
    class DummyResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"dummy": "data"}

    return DummyResponse()


def dummy_store_data(self, data):
    # Instead of calling DynamoDB, just return a dummy stored item.
    return {"id": "dummy-id", "data": data}


def test_lambda_handler(monkeypatch):
    # Monkeypatch requests.get so it doesn't perform a real HTTP call.
    monkeypatch.setattr("lambdas.hello_lambda.requests.get", dummy_get)

    # Monkeypatch DataIngestor.store_data to avoid actual DynamoDB calls.
    monkeypatch.setattr(DataIngestor, "store_data", dummy_store_data)

    response = lambda_handler({}, None)
    assert response["statusCode"] == 200
    body = json.loads(response["body"])

    # The expected response structure now has a message and stored_item.
    expected = {
        "message": "Data processed and stored",
        "stored_item": {"id": "dummy-id", "data": {"dummy": "data"}},
    }
    assert body == expected
