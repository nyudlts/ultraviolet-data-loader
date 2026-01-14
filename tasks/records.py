import glob
import json

import requests
from invoke import task

from tasks.helpers import (
    json_headers,
    octet_stream_headers,
    minimal_record,
    environment_config,
)


def initialize_and_commit_file(config, draft_id, file_path):
    print("Uploading file {0}...".format(file_path))

    file_name = file_path.split("/")[-1]
    file_data = [{"key": file_name}]

    file_initialize_url = "{0}/api/records/{1}/draft/files".format(
        config["BASE_URL"], draft_id
    )
    file_content_url = "{0}/api/records/{1}/draft/files/{2}/content".format(
        config["BASE_URL"], draft_id, file_name
    )
    file_commit_url = "{0}/api/records/{1}/draft/files/{2}/commit".format(
        config["BASE_URL"], draft_id, file_name
    )

    print("Initializing file...")
    initialize_file_response = requests.post(
        file_initialize_url,
        headers=json_headers(config["ACCESS_TOKEN"]),
        json=file_data,
        verify=False,
    )

    print(
        "Initialize File Response Code: {0}".format(
            initialize_file_response.status_code
        )
    )
    print("File Content URL: {0}".format(file_content_url))

    print("Uploading file...")
    with open(file_path, "rb") as file:
        file_upload_response = requests.put(
            file_content_url,
            headers=octet_stream_headers(config["ACCESS_TOKEN"]),
            data=file,
            stream=True,
            verify=False,
        )

    print("File Upload Response Code: {0}".format(file_upload_response.status_code))

    print("Committing file...")
    commit_response = requests.post(
        file_commit_url,
        headers=json_headers(config["ACCESS_TOKEN"]),
        verify=False,
    )
    print("Commit File Response Code: {0}".format(commit_response.status_code))
    print("")


@task(
    help={
        "environment": "Target UltraViolet environment",
        "data": "JSON string of metadata to create the record with",
    },
    optional=["environment", "data"],
)
def create_draft(_ctx, environment="local", data=minimal_record()):
    """
    Create a draft record
    """
    with environment_config(environment) as config:
        draft_response = requests.post(
            "{0}/api/records".format(config["BASE_URL"]),
            headers=json_headers(config["ACCESS_TOKEN"]),
            data=json.dumps(data),
            verify=False,
        )

        draft_response.raise_for_status()

        print("Draft Response Code: {0}".format(draft_response.status_code))

        draft_id = draft_response.json()["id"]
        print("Draft Record ID: {0}".format(draft_id))


@task(
    help={
        "draft-id": "The ID of the draft record to upload the file to",
        "file-path": "Path to the file to upload",
        "environment": "Target UltraViolet environment",
    },
    optional=["environment"],
)
def upload_file(_ctx, draft_id, file_path, environment="local"):
    """
    Upload a single file to a record
    """
    with environment_config(environment) as config:
        initialize_and_commit_file(config, draft_id, file_path)


@task(
    help={
        "draft-id": "The ID of the draft record to upload the file to",
        "glob-pattern": "Glob pattern of files to upload (*.jpg, code/*.py, etc.)",
        "environment": "Target UltraViolet environment",
    },
    optional=["environment"],
)
def upload_files(_ctx, draft_id, glob_pattern, environment="local"):
    """
    Upload multiple files to a record using glob patterns (*.jpg, code/*.py, etc.)
    """
    with environment_config(environment) as config:
        for file_path in glob.glob(glob_pattern):
            initialize_and_commit_file(config, draft_id, file_path)


@task
def publish(_ctx, draft_id, environment="local"):
    """
    Publish a draft record
    """
    with environment_config(environment) as config:
        publish_response = requests.post(
            "{0}/api/records/{1}/draft/actions/publish".format(
                config["BASE_URL"], draft_id
            ),
            headers=json_headers(config["ACCESS_TOKEN"]),
            verify=False,
        )

        publish_response.raise_for_status()

        print("Publish Response Code: {0}".format(publish_response.status_code))

        record_id = publish_response.json()["id"]
        print("Record ID: {0}".format(record_id))


@task(
    help={
        "environment": "Target UltraViolet environment",
    },
    optional=["environment"],
)
def test(_ctx, environment="local"):
    """
    Tests access to an environment by listing the number of records.
    """
    with environment_config(environment) as config:
        response = requests.get(
            "{0}/api/records".format(config["BASE_URL"]),
            headers=json_headers(config["ACCESS_TOKEN"]),
            verify=False,
        )

        print("{0} records found.".format(response.json()["hits"]["total"]))
