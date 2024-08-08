# pyThor

pyThor is a Python CLI and service that converts media files to H.265 format. It uses `ffmpeg` to perform the conversion and only keeps the video if the output file is smaller than the input file.

Name was a happy accident when typing python when writing the README, and therefore the name stuck.

## T.H.O.R.: Transformation and H.265 Optimization Resource

This service uses `ffmpeg` to perform media file conversions to H.265 format, which is more efficient than H.264. The script takes a media file as input and converts it to H.265 format with the same resolution and frame rate.

## Features

* Converts media files to H.265 format.
* Only keeps the video if the output file is smaller than the input file.
* Runs as a service (TBD)
* Fully configurable (TBD)
* Scans nested directories for media files (TBD)

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

### Example

```sh
poetry install
poetry shell
python convert.py input.mp4
```
