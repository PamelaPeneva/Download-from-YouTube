from yt_downloader import download_yt_dlp, download_ffmpeg, run_yt_dlp

if __name__ == "__main__":
    url = input("Enter YouTube URL: ").strip()
    yd_url = url if url else "https://youtu.be/JCN8qkWVu1w?si=OH6fV8jI-oGvBWLM"

    download_yt_dlp()
    download_ffmpeg()
    run_yt_dlp(yd_url)
    print("\nDone!")