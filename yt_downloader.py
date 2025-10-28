import subprocess
import os
import glob
import urllib.request
import zipfile
import shutil

DOWNLOAD_DIR = r"C:\Users\Public\yt-dlp-downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

YTDLP_EXE = os.path.join(DOWNLOAD_DIR, "yt-dlp.exe")
FFMPEG_DIR = os.path.join(DOWNLOAD_DIR, "ffmpeg")
FFMPEG_EXE = os.path.join(FFMPEG_DIR, "bin", "ffmpeg.exe")


def download_file(url, dest):
    print(f"Downloading: {url}")
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
        url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
        download_file(url, zip_path)

        print("Extracting FFmpeg...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(FFMPEG_DIR)

        # Find the extracted folder containing ffmpeg.exe
        ffmpeg_bin = None
        for root, dirs, files in os.walk(FFMPEG_DIR):
            if "ffmpeg.exe" in files:
                ffmpeg_bin = root
                break

        if ffmpeg_bin is None:
            raise FileNotFoundError("ffmpeg.exe not found after extraction!")

        dest_bin = os.path.join(FFMPEG_DIR, "bin")
        # Remove existing bin folder if it exists
        if os.path.exists(dest_bin):
            shutil.rmtree(dest_bin)

        shutil.move(ffmpeg_bin, dest_bin)
        os.remove(zip_path)
        print(f"FFmpeg ready at: {FFMPEG_EXE}")
    else:
        print(f"FFmpeg already exists: {FFMPEG_EXE}")


def run_yt_dlp(url):
    if not os.path.exists(YTDLP_EXE):
        raise FileNotFoundError("yt-dlp.exe not found! Run download_yt_dlp() first.")
    if not os.path.exists(FFMPEG_EXE):
        raise FileNotFoundError("ffmpeg.exe not found! Run download_ffmpeg() first.")

    cmd = [
        YTDLP_EXE,
        url,
        "--ffmpeg-location", FFMPEG_EXE,
        "-o", os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s"),
        "-f", "bestaudio/best",
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "0",
        "--embed-thumbnail",
        "--add-metadata",
        "--no-mtime",
        "--quiet",
        "--progress"
    ]

    subprocess.run(cmd, check=True)
    print(f"Download & conversion finished! Files saved in: {DOWNLOAD_DIR}")

    # Clean up leftover video files
    for vf in glob.glob(os.path.join(DOWNLOAD_DIR, "*.mp4")) + \
              glob.glob(os.path.join(DOWNLOAD_DIR, "*.webm")):
        os.remove(vf)
        print(f"Removed temporary video file: {vf}")


if __name__ == "__main__":
    download_yt_dlp()
    download_ffmpeg()
    url = input("Enter YouTube URL: ")
    run_yt_dlp(url)
