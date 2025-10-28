import os
import glob
import time
import unittest
import subprocess
import yt_downloader as yd

class TestYTDownloader(unittest.TestCase):
    TEST_URL = "https://youtu.be/JCN8qkWVu1w?si=OH6fV8jI-oGvBWLM"

    @classmethod
    def setUpClass(cls):
        print("\n==============================")
        print("Setting up YT Downloader Test")
        print("==============================")

        # Ensure download directory exists
        os.makedirs(yd.DOWNLOAD_DIR, exist_ok=True)

        # Ensure yt-dlp and ffmpeg are available
        yd.download_yt_dlp()
        yd.download_ffmpeg()

        assert os.path.exists(yd.YTDLP_EXE), "yt-dlp.exe missing!"
        assert os.path.exists(yd.FFMPEG_EXE), "ffmpeg.exe missing!"

        print("Tools verified.")

    def test_1_tools_exist(self):
        """Check that yt-dlp and ffmpeg are properly downloaded."""
        self.assertTrue(os.path.exists(yd.YTDLP_EXE), "yt-dlp.exe not found")
        self.assertTrue(os.path.exists(yd.FFMPEG_EXE), "ffmpeg.exe not found")
        print("yt-dlp and ffmpeg presence confirmed.")

    def test_2_download_and_convert(self):
        """Download and convert a test video to MP3."""
        print("\nRunning yt-dlp download test...")
        start_time = time.time()

        yd.run_yt_dlp(self.TEST_URL)

        mp3_files = glob.glob(os.path.join(yd.DOWNLOAD_DIR, "*.mp3"))
        self.assertTrue(mp3_files, "No MP3 file created by yt-dlp")

        mp3_path = mp3_files[0]
        print(f"MP3 created: {os.path.basename(mp3_path)}")

        # cleanup
        os.remove(mp3_path)
        print(f"Removed test MP3: {os.path.basename(mp3_path)}")

        print(f"Test completed in {round(time.time() - start_time, 2)} seconds.")

    @classmethod
    def tearDownClass(cls):
        """Run after all tests finish."""
        print("\nAll tests in TestYTDownloader completed.\n")


if __name__ == "__main__":
    # python test_downloader.py
    unittest.main(verbosity=2)
