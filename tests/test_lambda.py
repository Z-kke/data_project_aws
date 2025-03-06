import json

from lambdas.hello_lambda import DataIngestor, lambda_handler


def test_fetch_data(monkeypatch):
    # Dummy response class to simulate an API response
    class DummyResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"dummy": "data"}

    # Replace requests.get with a dummy function that returns our DummyResponse
    def dummy_get(url):
        return DummyResponse()

    monkeypatch.setattr("lambdas.hello_lambda.requests.get", dummy_get)

    ingestor = DataIngestor("http://dummy.url")
    data = ingestor.fetch_data()
    assert data == {"dummy": "data"}


def test_lambda_handler(monkeypatch):
    # Dummy response to be returned when lambda_handler calls requests.get
    class DummyResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"dummy": "data"}

    def dummy_get(url):
        return DummyResponse()

    monkeypatch.setattr("lambdas.hello_lambda.requests.get", dummy_get)

    response = lambda_handler({}, None)
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body == {"dummy": "data"}
