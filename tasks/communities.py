import json
import os

import requests
import urllib3
from dotenv import dotenv_values
from invoke import task
from requests import HTTPError

from tasks.helpers import json_headers


@task(
    help={
        "environment": "Target UltraViolet environment",
    },
    optional=["environment"],
)
def list_all(_ctx, environment="local"):
    """
    Lists all Communities
    """
    urllib3.disable_warnings(category=urllib3.exceptions.InsecureRequestWarning)

    environment_file = "environments/{0}.env".format(environment)

    if os.path.isfile(environment_file):
        config = dotenv_values(environment_file)

        response = requests.get(
            "{0}/api/communities".format(config["BASE_URL"]),
            headers=json_headers(config["ACCESS_TOKEN"]),
            verify=False,
        )

        hits = response.json()["hits"]["hits"]
        for hit in hits:
            print("\n# {0} ({1})\n".format(hit["metadata"]["title"], hit["slug"]))
            print("Subcommunities: {0}".format(hit["children"]["allow"]))


@task(
    help={
        "slug": "Slug of the environment you want to view",
        "environment": "Target UltraViolet environment",
    },
    optional=["environment"],
)
def show(_ctx, slug, environment="local"):
    """
    Displays the output of a single community
    """
    urllib3.disable_warnings(category=urllib3.exceptions.InsecureRequestWarning)

    environment_file = "environments/{0}.env".format(environment)

    if os.path.isfile(environment_file):
        config = dotenv_values(environment_file)

        response = requests.get(
            "{0}/api/communities/{1}".format(config["BASE_URL"], slug),
            verify=False,
        )

        print(json.dumps(response.json(), indent=2))


@task(
    help={
        "slug": "Slug of the environment you want to update",
        "environment": "Target UltraViolet environment",
    },
    optional=["environment"],
)
def enable_subcommunities(_ctx, slug, environment="local"):
    """
    Enables subcommunities on the given top-level community
    """
    urllib3.disable_warnings(category=urllib3.exceptions.InsecureRequestWarning)

    environment_file = "environments/{0}.env".format(environment)

    if os.path.isfile(environment_file):
        config = dotenv_values(environment_file)

        get_response = requests.get(
            "{0}/api/communities/{1}".format(config["BASE_URL"], slug),
            headers=json_headers(config["ACCESS_TOKEN"]),
            verify=False,
        )

        response_json = get_response.json()

        new_subcommunities_url = "You can create new communities at {0}/communities/{1}/subcommunities/new".format(
            config["BASE_URL"], slug
        )

        if response_json["children"]["allow"]:
            print("Subcommunities already enabled for {0}.".format(slug))
            print(new_subcommunities_url)

        else:
            update_data = {
                "slug": slug,
                "metadata": response_json["metadata"],
                "access": response_json["access"],
                "children": {"allow": "yes"},
            }

            try:
                update_response = requests.put(
                    "{0}/api/communities/{1}".format(config["BASE_URL"], slug),
                    headers=json_headers(config["ACCESS_TOKEN"]),
                    verify=False,
                    data=json.dumps(update_data),
                )
                update_response.raise_for_status()
                print(new_subcommunities_url)

            except HTTPError as e:
                print(e.response.text)

            print("Update Response Code: {0}".format(get_response.status_code))
