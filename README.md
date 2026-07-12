# MP4 to HLS Automation

## Overview

This project automates the MP4 to HLS conversion process using Python.

## Features

* Comprehensive logging for every workflow step.
* Creates a tmux session before executing FFmpeg.
* Executes FFmpeg using Python's subprocess module.
* Generates HLS output (`master.m3u8` and `.ts` segment files).
* Logs all generated `.ts` files.

## Project Structure

```text
mp4-to-hls/
├── hls.py
├── README.md
├── input/
├── output/
├── logs/
└── .gitignore
```

## Requirements

* Python 3
* FFmpeg
* tmux
* Ubuntu / WSL

## How to Run

1. Place the input video as `input/sample.mp4`.
2. Run:

```bash
python3 hls.py
```

## Output

The script generates:

* `master.m3u8`
* `.ts` segment files
* `logs/hls.log`

## Technologies Used

* Python
* FFmpeg
* tmux
* Linux (WSL)
README

