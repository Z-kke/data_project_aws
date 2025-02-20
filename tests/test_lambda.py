from lambdas.hello_lambda import lambda_handler


def test_lambda_handler():
    event = {}  # Dummy event
    context = None  # Dummy context
    response = lambda_handler(event, context)
    assert response["statusCode"] == 200
    assert "Hello" in response["body"]
