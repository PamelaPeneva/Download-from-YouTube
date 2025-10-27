import subprocess
import os
import sys
import glob
import urllib.request
import zipfile

# ===============================
# CONFIGURATION
# ===============================

DOWNLOAD_DIR = r"C:\Users\Public\yt-dlp-downloads"  # Change this
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

YTDLP_EXE = os.path.join(DOWNLOAD_DIR, "yt-dlp.exe")
FFMPEG_DIR = os.path.join(DOWNLOAD_DIR, "ffmpeg")
FFMPEG_EXE = os.path.join(FFMPEG_DIR, "bin", "ffmpeg.exe")

URL = "https://youtu.be/JCN8qkWVu1w?si=OH6fV8jI-oGvBWLM"  # URL here

# ===============================
# FUNCTION TO DOWNLOAD FILES
# ===============================

def download_file(url, dest):
    print(f"⬇ Downloading: {url}")
    urllib.request.urlretrieve(url, dest)
    print(f"Saved to: {dest}")

def download_yt_dlp():
    if not os.path.exists(YTDLP_EXE):
        url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"
        download_file(url, YTDLP_EXE)
    else:
        print(f"yt-dlp already exists: {YTDLP_EXE}")

def download_ffmpeg():
    if not os.path.exists(FFMPEG_EXE):
        zip_path = os.path.join(DOWNLOAD_DIR, "ffmpeg.zip")
        # Essentials build from Gyan
        url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
        download_file(url, zip_path)
        print("Extracting FFmpeg...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(FFMPEG_DIR)
        # Move the bin folder to FFMPEG_DIR
        for root, dirs, files in os.walk(FFMPEG_DIR):
            if "ffmpeg.exe" in files:
                ffmpeg_bin = root
                os.rename(ffmpeg_bin, os.path.join(FFMPEG_DIR, "bin"))
                break
        os.remove(zip_path)
        print(f"FFmpeg ready at: {FFMPEG_EXE}")
    else:
        print(f"FFmpeg already exists: {FFMPEG_EXE}")

# ===============================
# DOWNLOAD TOOLS IF NEEDED
# ===============================

download_yt_dlp()
download_ffmpeg()

# ===============================
# BUILD YT-DLP COMMAND
# ===============================

cmd = [
    YTDLP_EXE,
    URL,
    "--ffmpeg-location", FFMPEG_EXE,
    "-o", os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s"),
    "-f", "bestaudio/best",
    "--extract-audio",
    "--audio-format", "mp3",
    "--audio-quality", "0",
    "--embed-thumbnail",
    "--add-metadata",
    "--no-mtime",
    "--verbose"
]

# ===============================
# RUN COMMAND
# ===============================

try:
    subprocess.run(cmd, check=True)
    print(f"\nDownload & conversion finished! File saved in: {DOWNLOAD_DIR}")

    # Remove leftover video files
    video_files = glob.glob(os.path.join(DOWNLOAD_DIR, "*.mp4")) + \
                  glob.glob(os.path.join(DOWNLOAD_DIR, "*.webm"))
    for vf in video_files:
        os.remove(vf)
        print(f"Removed temporary video file: {vf}")

except subprocess.CalledProcessError as e:
    print(f"\nyt-dlp failed with exit code {e.returncode}")
