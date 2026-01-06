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
$ invoke records.upload-file --environment=qa --draft-id=exeph-73h23 --file-path=tasks/records.py
$ invoke records.upload-file -e qa -d exeph-73h23 -f tasks/records.py
$ invoke records.upload-file qa exeph-73h23 tasks/records.py
```

#### Upload Files

Upload multiple files to a draft record.

```bash
$ invoke records.upload-files --environment=qa --draft-id=vhtmn-sw870 --glob-pattern="data/*.wacz"
$ invoke records.upload-files -e qa -d vhtmn-sw870 -g "data/*.wacz"
$ invoke records.upload-files qa vhtmn-sw870 "data/*.wacz"
```
