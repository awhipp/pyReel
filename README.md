# pyReel

[![Pre-commit Checks](https://github.com/awhipp/pyReel/actions/workflows/pre-commit-check.yml/badge.svg)](https://github.com/awhipp/pyReel/actions/workflows/pre-commit-check.yml)

pyReel is a Python service that converts media files to H.265 format. It uses `ffmpeg` to perform the conversion and only keeps the video if the output file is smaller than the input file.

## R.E.E.L.: Rapid & Efficient Encoding Library

This service uses `ffmpeg` to perform media file conversions to H.265 format, which is more efficient than H.264. The script takes a media file as input and converts it to H.265 format with the same resolution and frame rate.

## Features

* Converts media files to H.265 format.
* Only keeps the video if the output file is smaller than the input file.
* Runs as an API service
* Fully configurable (TBD)
* Scans nested directories for media files

## Prerequisites

- Python 3.x
- `ffmpeg` installed on your system

## Installation

### Installing Python

If you don't have Python installed, you can download it from [python.org](https://www.python.org/downloads/).

### Installing ffmpeg

On a Linux machine, you can install `ffmpeg` using the following command:

```sh
sudo apt-get update
sudo apt-get install ffmpeg
```

For other operating systems, please refer to the official ffmpeg installation guide.

## Usage

1. Clone the repository or download the convert.py script.
2. Ensure ffmpeg is installed and accessible from the command line.
3. Run the script using Python.

### Environment Variables

* `ROOT_DIR` - The root directory to scan for media files. Default is the current directory.
* `SQLITE_DB` - The SQLite database file to store the conversion results. Default is `files.db`.

### Development

#### Pre-commit and Githooks

Installing pre-commit and running the hooks

```sh
pre-commit install
pre-commit run --all-files
```

#### Running the FastAPI service locally

```sh
poetry install
poetry shell
uvicorn app:app --reload
```
