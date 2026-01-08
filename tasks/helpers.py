def json_headers(ACCESS_TOKEN):
    return {
        "Authorization": "Bearer {0}".format(ACCESS_TOKEN),
        "Content-Type": "application/json",
    }


def octet_stream_headers(ACCESS_TOKEN):
    return {
        "Authorization": "Bearer {0}".format(ACCESS_TOKEN),
        "Content-Type": "application/octet-stream",
    }


def minimal_record():
    return {
        "access": {"record": "public", "files": "public"},
        "files": {"enabled": True},
        "metadata": {
            "creators": [
                {
                    "person_or_org": {
                        "family_name": "Dent",
                        "given_name": "Arthur",
                        "type": "personal",
                    }
                },
            ],
            "publisher": "Megadodo Publications",
            "publication_date": "2020-06-01",
            "resource_type": {"id": "image-photo"},
            "title": "On Sandwhich Making",
        },
    }
