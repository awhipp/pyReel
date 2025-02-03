# pyReel

## R.E.E.L.: Rapid & Efficient Encoding Library

pyReel is a Python service that converts media files to H.265 format. It uses `ffmpeg` to perform the conversion and only keeps the video if the output file is smaller than the input file.

## CI/CD

[![UI / Node Tests](https://github.com/awhipp/pyReel/actions/workflows/ui-tests.yml/badge.svg)](https://github.com/awhipp/pyReel/actions/workflows/ui-tests.yml)

[![API / Python Tests](https://github.com/awhipp/pyReel/actions/workflows/api-tests.yml/badge.svg)](https://github.com/awhipp/pyReel/actions/workflows/api-tests.yml)

[![Pre-commit Checks](https://github.com/awhipp/pyReel/actions/workflows/pre-commit-check.yml/badge.svg)](https://github.com/awhipp/pyReel/actions/workflows/pre-commit-check.yml)

[![CodeQL](https://github.com/awhipp/pyReel/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/awhipp/pyReel/actions/workflows/github-code-scanning/codeql)

## Features

* Converts media files to H.265 format.
* Only keeps the video if the output file is smaller than the input file.
* Runs as an API service
* Fully configurable (TBD)
* Scans nested directories for media files

## Pre-requisites

### Mandatory

* Node 22 (LTS)
* Python 3.10^
* ffmpeg
* poetry

### Recommended

* Precommit

## Frontend

The frontend is a React application that allows users to manage and convert media files. It uses the backend service to perform the conversion.

### Setup Frontend Locally

```sh
cd ui/
npm install
npm run start
```

## Backend

The backend is a FastAPI service that converts media files to H.265 format. It uses `ffmpeg` to perform the conversion and only keeps the video if the output file is smaller than the input file.

### Setup Backend Locally

Once prereqs are installed, you can begin setting up the project.

#### Environment Variables

* `ROOT_DIR` - The root directory to scan for media files. Default is the current directory.
* `SQLITE_DB` - The SQLite database file to store the conversion results. Default is `pyreel.db`.

#### Pre-commit and Githooks

Installing pre-commit and running the hooks

```sh
pre-commit install
pre-commit run --all-files
```

#### Running the backend service locally

```sh
cd /api
poetry install
poetry shell
uvicorn app:app --reload
```

### Testing Backend

To run the tests, run the following command:

```sh
cd /api
pytest
```
