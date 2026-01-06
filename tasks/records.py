import glob
import json
import os
from contextlib import contextmanager

import requests
import urllib3
from dotenv import dotenv_values
from invoke import task

from tasks.helpers import json_headers, octet_stream_headers, minimal_record


@task(
    help={
        "environment": "Target UltraViolet environment",
        "data": "JSON string of metadata to create the record with"
    },
    optional=["environment", "data"],
)
def create_draft(
        _ctx,
        environment="local",
        data=minimal_record()
):
    """
    Create a draft record
    """
    urllib3.disable_warnings(category=urllib3.exceptions.InsecureRequestWarning)

    environment_file = "environments/{0}.env".format(environment)

    if os.path.isfile(environment_file):
        config = dotenv_values(environment_file)

        draft_response = requests.post(
            "{0}/api/records".format(config["BASE_URL"]),
            headers=json_headers(config["BEARER_TOKEN"]),
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
    urllib3.disable_warnings(category=urllib3.exceptions.InsecureRequestWarning)

    environment_file = "environments/{0}.env".format(environment)

    if os.path.isfile(environment_file):
        config = dotenv_values(environment_file)

        file_name = file_path.split("/")[-1]
        file_data = [{"key": file_name}]

        print("Initializing file...")
        initialize_file_response = requests.post(
            "{0}/api/records/{1}/draft/files".format(config["BASE_URL"], draft_id),
            headers=json_headers(config["BEARER_TOKEN"]),
            json=file_data,
            verify=False,
        )

        print("Initialize File Response Code: {0}".format(initialize_file_response.status_code))

        initialize_json = json.loads(initialize_file_response.content)
        file_content_url = initialize_json["entries"][0]["links"]["content"]
        file_commit_url = initialize_json["entries"][0]["links"]["commit"]

        print("File Content URL: {0}".format(file_content_url))

        print("Uploading file...")
        with open(file_path, "rb") as file:
            file_upload_response = requests.put(
                file_content_url,
                headers=octet_stream_headers(config["BEARER_TOKEN"]),
                data=file,
                stream=True,
                verify=False
            )

        print("File Upload Response Code: {0}".format(file_upload_response.status_code))

        print("Committing file...")
        commit_response = requests.post(
            file_commit_url,
            headers=(json_headers(config["BEARER_TOKEN"])),
            verify=False,
        )
        print("Commit File Response Code: {0}".format(commit_response.status_code))


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
    urllib3.disable_warnings(category=urllib3.exceptions.InsecureRequestWarning)

    environment_file = "environments/{0}.env".format(environment)

    if os.path.isfile(environment_file):
        config = dotenv_values(environment_file)

        for file_path in glob.glob(glob_pattern):
            print("Uploading file {0}...".format(file_path))
            file_name = file_path.split("/")[-1]
            file_data = [{"key": file_name}]

            print("Initializing file...")
            initialize_file_response = requests.post(
                "{0}/api/records/{1}/draft/files".format(config["BASE_URL"], draft_id),
                headers=json_headers(config["BEARER_TOKEN"]),
                json=file_data,
                verify=False,
            )

            print("Initialize File Response Code: {0}".format(initialize_file_response.status_code))

            initialize_json = json.loads(initialize_file_response.content)
            file_content_url = initialize_json["entries"][0]["links"]["content"]
            file_commit_url = initialize_json["entries"][0]["links"]["commit"]

            print("File Content URL: {0}".format(file_content_url))

            print("Uploading file...")
            with open(file_path, "rb") as file:
                file_upload_response = requests.put(
                    file_content_url,
                    headers=octet_stream_headers(config["BEARER_TOKEN"]),
                    data=file,
                    stream=True,
                    verify=False
                )

            print("File Upload Response Code: {0}".format(file_upload_response.status_code))

            print("Committing file...")
            commit_response = requests.post(
                file_commit_url,
                headers=json_headers(config["BEARER_TOKEN"]),
                verify=False,
            )
            print("Commit File Response Code: {0}".format(commit_response.status_code))
            print("")


@contextmanager
def load_environment(environment):
    environment_file = "environments/{0}.env".format(environment)

    if os.path.isfile(environment_file):
        config = dotenv_values(environment_file)
        yield config
    else:
        print("Environment {0} not found. Exiting...".format(environment))


@task(
    help={
        "environment": "Target UltraViolet environment",
    },
    optional=["environment"]
)
def test(_ctx, environment="local"):
    """
    Tests access to an environment by listing the number of records.
    """
    urllib3.disable_warnings(category=urllib3.exceptions.InsecureRequestWarning)

    environment_file = "environments/{0}.env".format(environment)

    if os.path.isfile(environment_file):
        config = dotenv_values(environment_file)

        response = requests.get(
            "{0}/api/records".format(config["BASE_URL"]),
            headers=json_headers(config["BEARER_TOKEN"]),
            verify=False
        )

        print("{0} records found.".format(response.json()["hits"]["total"]))

    else:
        print("ERROR: Environment '{0}' not found".format(environment))
