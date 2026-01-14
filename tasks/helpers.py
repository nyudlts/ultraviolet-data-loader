import os
from contextlib import contextmanager

from dotenv import dotenv_values


@contextmanager
def environment_config(environment):
    environment_file = "environments/{0}.env".format(environment)

    if os.path.isfile(environment_file):
        yield dotenv_values(environment_file)
    else:
        raise RuntimeError(
            "Environment file not found - {0}".format(environment_file)
        ) from None


def json_headers(access_token):
    return {
        "Authorization": "Bearer {0}".format(access_token),
        "Content-Type": "application/json",
    }


def octet_stream_headers(access_token):
    return {
        "Authorization": "Bearer {0}".format(access_token),
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
            "title": "On Sandwich Making",
        },
    }
