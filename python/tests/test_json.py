import pytest
import requests


@pytest.mark.parametrize(
    "key, payload, expected",
    [
        (
            "strData",
            '<div class="div-class"></div>',
            '\\u003cdiv class\\u003d"div-class"\\u003e\\u003c/div\\u003e',
        )
    ],
)
def test_escape_html(rest_client, key, payload, expected):
    data = {key: payload}
    response = rest_client.post("/predict", json=data)
    response = response.get_json()

    escaped = response[key]
    assert escaped == expected
