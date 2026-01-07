from tasks.helpers import json_headers, octet_stream_headers


def test_json_headers():
    headers = json_headers("foobar")

    assert headers == {
        "Authorization": "Bearer foobar",
        "Content-Type": "application/json",
    }


def test_octet_stream_headers():
    headers = octet_stream_headers("foobar")

    assert headers == {
        "Authorization": "Bearer foobar",
        "Content-Type": "application/octet-stream",
    }
