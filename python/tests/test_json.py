import pytest
import requests

from seldon_core.json import htmlescape_dumps


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


@pytest.mark.parametrize(
    "payload, expected",
    [
        (
            {"strData": '<div class="div-class"></div>'},
            '{"strData": "\\u003cdiv class=\\"div-class\\"\\u003e\\u003c/div\\u003e"}',
        ),
        (
            '<div class="div-class"></div>',
            '\\u003cdiv class=\\"div-class\\"\\u003e\\u003c/div\\u003e',
        ),
        (
            {"jsonData": {"someHTML": '<div class="div-class"></div>'}},
            '{"jsonData": {"someHTML": "\\u003cdiv class=\\"div-class\\"\\u003e\\u003c/div\\u003e"}}',
        ),
        ({"data": {"ndarray": [0, 1, 2]}}, '{"data": {"ndarray": [0, 1, 2]}}',),
    ],
)
def test_htmlescape_dumps(payload, expected):
    escaped = htmlescape_dumps(payload)
    assert escaped == expected
