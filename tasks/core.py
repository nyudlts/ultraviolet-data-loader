import os

from invoke import task

INVENIO_ENVIRONMENTS = ["local", "development", "qa", "production"]


@task(aliases=["init"])
def initialize(_ctx):
    """
    Initialize the project's environment configuration files.
    """
    [initialize_invenio_environment(e) for e in INVENIO_ENVIRONMENTS]


def initialize_invenio_environment(environment):
    write_environment_file(
        "environments/{0}.env".format(environment),
        """\
BEARER_TOKEN=insert_token_here
BASE_URL=https://127.0.0.1:5000
        """,
    )


def write_environment_file(environment_file, template):
    if os.path.isfile(environment_file):
        print("Warning: configuration file {0} already exists".format(environment_file))
    else:
        file = open(environment_file, "w")
        file.write(template)
        file.close()
        print("{0} created.".format(environment_file))
