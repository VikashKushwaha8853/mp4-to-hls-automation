import os
import logging
import subprocess
import glob
import time

# Configure logging
logging.basicConfig(
    filename="logs/hls.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

print("HLS Automation Started")
logging.info("========== HLS Automation Started ==========")

# Check input file
input_file = "input/sample.mp4"

if os.path.exists(input_file):
    print("Input video found")
    logging.info(f"Input video found: {input_file}")
else:
    print("Input video not found")
    logging.error(f"Input video not found: {input_file}")
    exit()

# Ensure output folder exists
os.makedirs("output", exist_ok=True)
logging.info("Output directory verified")

print("Setup completed successfully")
logging.info("Setup completed successfully")
# Create tmux session
session_name = "hls_session"

logging.info(f"Creating tmux session: {session_name}")

result = subprocess.run(
    ["tmux", "new-session", "-d", "-s", session_name],
    capture_output=True,
    text=True
)

if result.returncode == 0:
    print("tmux session created successfully")
    logging.info("tmux session created successfully")
else:
    print("Failed to create tmux session")
    print(result.stderr)
    logging.error(result.stderr)
    exit()
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

logging.info("Starting FFmpeg inside tmux")

subprocess.run([
    "tmux",
    "send-keys",
    "-t",
    session_name,
    ffmpeg_command,
    "C-m"
])

print("FFmpeg command sent to tmux")
logging.info("FFmpeg command sent to tmux")
# Wait for FFmpeg to finish
time.sleep(5)

logging.info("Checking generated TS files")

ts_files = sorted(glob.glob("output/*.ts"))

if ts_files:
    logging.info("Generated TS files:")

    for file in ts_files:
        filename = os.path.basename(file)
        print(filename)
        logging.info(filename)

    logging.info("HLS conversion completed successfully")
else:
    logging.error("No TS files were generated")
