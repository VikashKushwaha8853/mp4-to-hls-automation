import os
import logging
import subprocess
import glob
import time
import sys
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename="logs/hls.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Start Time
start_time = datetime.now()

print("HLS Automation Started")
logging.info("=" * 60)
logging.info("HLS Automation Started")
logging.info(f"Process Start Time : {start_time}")

# Input File
input_file = "input/sample.mp4"

if not os.path.exists(input_file):
    print("Input video not found")
    logging.error(f"Input video not found : {input_file}")
    logging.error("Status : FAILED")
    sys.exit(1)

print("Input video found")
logging.info(f"Input File : {input_file}")

file_size = os.path.getsize(input_file)
logging.info(f"Input File Size : {file_size} bytes")

# Output Directory
os.makedirs("output", exist_ok=True)
logging.info("Output directory verified")

# tmux Session
session_name = "hls_session"

# Remove old session if exists
subprocess.run(
    ["tmux", "kill-session", "-t", session_name],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

logging.info(f"Creating tmux session : {session_name}")

result = subprocess.run(
    ["tmux", "new-session", "-d", "-s", session_name],
    capture_output=True,
    text=True
)

if result.returncode != 0:
    logging.error("Failed to create tmux session")
    logging.error(result.stderr)
    sys.exit(1)

logging.info("tmux session created successfully")
# FFmpeg Command
ffmpeg_command = (
    "ffmpeg -y "
    "-i input/sample.mp4 "
    "-c:v libx264 "
    "-c:a aac "
    "-hls_time 6 "
    "-hls_playlist_type vod "
    "-hls_segment_filename output/%d.ts "
    "output/master.m3u8"
)

logging.info("FFmpeg Command:")
logging.info(ffmpeg_command)

# Run FFmpeg inside tmux
logging.info("Starting FFmpeg inside tmux")

result = subprocess.run(
    [
        "tmux",
        "send-keys",
        "-t",
        session_name,
        ffmpeg_command,
        "C-m"
    ],
    capture_output=True,
    text=True
)

if result.returncode != 0:
    logging.error("Failed to send FFmpeg command")
    logging.error(result.stderr)
    logging.error("Status : FAILED")
    sys.exit(1)

print("FFmpeg command sent to tmux")
logging.info("FFmpeg command sent successfully")

# Wait for conversion
time.sleep(5)

logging.info("Checking generated TS files")

ts_files = sorted(glob.glob("output/*.ts"))
if ts_files:
    logging.info("Generated TS Files:")

    for file in ts_files:
        filename = os.path.basename(file)
        print(filename)
        logging.info(filename)

    logging.info("Status : SUCCESS")
else:
    logging.error("No TS files were generated")
    logging.error("Status : FAILED")

# Output Location
logging.info(f"Output Location : {os.path.abspath('output')}")

# Process End Time
end_time = datetime.now()

logging.info(f"Process End Time : {end_time}")
logging.info("=" * 60)

# Close tmux session
subprocess.run(
    ["tmux", "kill-session", "-t", session_name],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

print("HLS Automation Completed")
