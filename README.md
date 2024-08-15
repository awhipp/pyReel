# pyReel

## R.E.E.L.: Rapid & Efficient Encoding Library

pyReel is a Python service that converts media files to H.265 format. It uses `ffmpeg` to perform the conversion and only keeps the video if the output file is smaller than the input file.

## CI/CD

[![Python Tests](https://github.com/awhipp/pyReel/actions/workflows/run-pytest.yml/badge.svg)](https://github.com/awhipp/pyReel/actions/workflows/run-pytest.yml) [![Pre-commit Checks](https://github.com/awhipp/pyReel/actions/workflows/pre-commit-check.yml/badge.svg)](https://github.com/awhipp/pyReel/actions/workflows/pre-commit-check.yml) [![CodeQL](https://github.com/awhipp/pyReel/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/awhipp/pyReel/actions/workflows/github-code-scanning/codeql)

## Features

* Converts media files to H.265 format.
* Only keeps the video if the output file is smaller than the input file.
* Runs as an API service
* Fully configurable (TBD)
* Scans nested directories for media files

## Frontend

The frontend is a React application that allows users to manage and convert media files. It uses the backend service to perform the conversion.

### Frontend Pre-requisites

Before you begin, ensure you have met the following requirements:

* Installed Node.js and npm

#### node and npm

If you don't have node and npm installed, you can download it from [nodejs.org](https://nodejs.org/en/download/package-manager/current).


### Setup Frontend Locally

```sh
cd ui/
npm install
npm run start
```

## Backend

The backend is a FastAPI service that converts media files to H.265 format. It uses `ffmpeg` to perform the conversion and only keeps the video if the output file is smaller than the input file.

### Backend Pre-requisites

Before you begin, ensure you have met the following requirements:

* Installed Python 3.10+
* Installed `ffmpeg`

#### Python 3.10+

If you don't have Python installed, you can download it from [python.org](https://www.python.org/downloads/).

#### ffmpeg

On a Linux machine, you can install `ffmpeg` using the following command:

```sh
sudo apt-get update
sudo apt-get install ffmpeg
```

For other operating systems, please refer to the official ffmpeg installation guide.

### Setup Backend Locally

Once prereqs are installed, you can begin setting up the project.

#### Environment Variables

* `ROOT_DIR` - The root directory to scan for media files. Default is the current directory.
* `SQLITE_DB` - The SQLite database file to store the conversion results. Default is `files.db`.

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
