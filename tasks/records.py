import glob
import json
import os
import sys
from json import JSONDecodeError

import requests
from invoke import task
from tasks.loader import Loader

from tasks.helpers import (
    json_headers,
    octet_stream_headers,
    minimal_record,
    environment_config,
)


def initialize_and_commit_file(config, draft_id, file_path):
    file_name = file_path.split("/")[-1]
    file_data = [{"key": file_name}]

    log_dir             = os.path.join("logs", "uploads", str(draft_id))
    success_log_path    = os.path.join(log_dir, "success.txt")
    fail_log_path       = os.path.join(log_dir, "fail.txt")

    # skip if the file has already been uploaded successfully
    if os.path.exists(success_log_path):
        with open(success_log_path, "r") as log_file:
            if file_name in log_file.read().splitlines():
                print("Skipping {0} - already uploaded successfully.".format(file_name))
                return
            

    os.makedirs(log_dir, exist_ok=True)
    print("Starting {0}...".format(file_name))

    file_initialize_url = "{0}/api/records/{1}/draft/files".format(
        config["BASE_URL"], draft_id
    )
    file_content_url = "{0}/api/records/{1}/draft/files/{2}/content".format(
        config["BASE_URL"], draft_id, file_name
    )
    file_commit_url = "{0}/api/records/{1}/draft/files/{2}/commit".format(
        config["BASE_URL"], draft_id, file_name
    )

    # initialize the file
    with Loader("\tInitializing file...", ""):
        initialize_file_response = requests.post(
            file_initialize_url,
            headers=json_headers(config["ACCESS_TOKEN"]),
            json=file_data,
            verify=False,
        )

    # upload the file content
    with Loader("\tUploading file...", ""):
        with open(file_path, "rb") as file:
            file_upload_response = requests.put(
                file_content_url,
                headers=octet_stream_headers(config["ACCESS_TOKEN"]),
                data=file,
                stream=True,
                verify=False,
            )
    
    # if the upload failed, log the failure and return
    if file_upload_response.status_code != 200:
        print("\tUpload Error: {0}".format(file_upload_response.json()))
        with open(fail_log_path, "a") as log_file:
            log_file.write("{0}\n".format(file_name))
        return
    
    # if the upload succeeded, wait 5 seconds before committing the file
    with Loader("\tWaiting 5 seconds before commit...", ""):
        import time
        time.sleep(5)

    # commit the file
    with Loader("\tCommitting file...", ""):
        commit_response = requests.post(
            file_commit_url,
            headers=json_headers(config["ACCESS_TOKEN"]),
            verify=False,
        )
        
    # if the commit failed, log the failure, otherwise log the success
    if commit_response.status_code != 200:
        print("\tCommit Error: {0}".format(commit_response.json()))
        with open(fail_log_path, "a") as log_file:
            log_file.write("{0}\n".format(file_name))
    else:
        print("\tDone ✔")
        with open(success_log_path, "a") as log_file:
            log_file.write("{0}\n".format(file_name))
@task(
    help={
        "environment": "Target UltraViolet environment",
        "file-path": "Path to JSON file containing the record data. If not provided, a minimal record will be created.",
    },
    optional=["environment", "file_path"],
)
def create_draft(_ctx, environment="local", file_path=None):
    """
    Create a draft record
    """
    with environment_config(environment) as config:
        data = ""

        if file_path is None:
            data = json.dumps(minimal_record())
        else:
            with open(file_path, "r") as file:
                data = file.read()

                try:
                    json.loads(data)
                except JSONDecodeError as err:
                    print("Error parsing {0} - {1}".format(file_path, err))
                    sys.exit(1)

        draft_response = requests.post(
            "{0}/api/records".format(config["BASE_URL"]),
            headers=json_headers(config["ACCESS_TOKEN"]),
            data=data,
            verify=False,
        )

        draft_response.raise_for_status()

        print("Draft Response Code: {0}".format(draft_response.status_code))

        draft_id = draft_response.json()["id"]
        print("Draft Record ID: {0}".format(draft_id))
        
        if file_path is not None:
            file_name = os.path.splitext(os.path.basename(file_path))[0]
            print("Draft Record Name: {0}".format(file_name))
            log_dir = os.path.join("logs", "drafts")
            os.makedirs(log_dir, exist_ok=True)
            log_path = os.path.join(log_dir, "{0}.txt".format(draft_id))
            with open(log_path, "w") as log_file:
                log_file.write("{0}\n".format(file_name))


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
