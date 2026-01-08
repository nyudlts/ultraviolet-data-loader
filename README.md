# UltraViolet Data Loader

A collection of tasks for testing and accessing UltraViolet instances.

## Getting Started

### Project Setup

To check out the project and prepate your local environment, do the following:

```bash
$ git clone git@github.com:nyudlts/ultraviolet-data-loader.git
$ cd ultraviolet-data-loader
$ pipenv install
$ pipenv shell
$ invoke initialize
```

Then you'll want to update the generated `environments/*.env` files with the correct values for each configuration variable.

## Tasks

To view the list of available tasks use `invoke --list`.

To view help on a particular tasks use `invoke --help <task_name>`.

### Initialize

Initialize the project's environment configuration files.

You should only need to do this once.

```bash
$ invoke initialize
```

### Records

#### Create Draft

Creates a draft record and provides its Draft ID.

```bash
$ invoke records.create-draft --environment=qa
$ invoke records.create-draft -e qa
$ invoke records.create-draft qa
```

#### Upload File

Upload a single file to a draft record.

```bash
$ invoke records.upload-file --draft-id=exeph-73h23 --file-path=tasks/records.py --environment=qa
$ invoke records.upload-file qa -d exeph-73h23 -f tasks/records.py -e
$ invoke records.upload-file exeph-73h23 tasks/records.py qa
```

#### Upload Files

Upload multiple files to a draft record.

```bash
$ invoke records.upload-files --draft-id=vhtmn-sw870 --glob-pattern="data/*.wacz" --environment=qa
$ invoke records.upload-files -d vhtmn-sw870 -g "data/*.wacz" -e qa
$ invoke records.upload-files vhtmn-sw870 "data/*.wacz" qa
```

## Development

### Tests

To run tests, using the following command:

```bash
$ pipenv run python -m pytest
```
