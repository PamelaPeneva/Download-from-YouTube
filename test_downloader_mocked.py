import os
import glob
import unittest
from unittest import mock
import yt_downloader as yd

# mocked yt-dlp ffmpeg and run_yt_dlp

class TestYTDownloader(unittest.TestCase):
    TEST_URL = "https://youtu.be/JCN8qkWVu1w?si=OH6fV8jI-oGvBWLM"

    @classmethod
    @mock.patch("yt_downloader.download_yt_dlp")
    @mock.patch("yt_downloader.download_ffmpeg")
    def setUpClass(cls, mock_ffmpeg, mock_yt_dlp):
        """
        Prepare environment for testing without downloading anything.
        Simulate the presence of yt-dlp.exe and ffmpeg.exe.
        """
        print("\n==============================")
        print("Setting up YT Downloader Test (mocked)")
        print("==============================")

        os.makedirs(yd.DOWNLOAD_DIR, exist_ok=True)
        os.makedirs(os.path.join(yd.FFMPEG_DIR, "bin"), exist_ok=True)

        # Create fake yt-dlp.exe and ffmpeg.exe
        with open(yd.YTDLP_EXE, "w") as f:
            f.write("fake yt-dlp executable")
        with open(yd.FFMPEG_EXE, "w") as f:
            f.write("fake ffmpeg executable")

        # Patch functions so they do nothing
        mock_yt_dlp.return_value = None
        mock_ffmpeg.return_value = None

        print(f"Fake tools created: {yd.YTDLP_EXE}, {yd.FFMPEG_EXE}")

    def test_1_tools_exist(self):
        """Verify fake yt-dlp and ffmpeg exist."""
        self.assertTrue(os.path.exists(yd.YTDLP_EXE))
        self.assertTrue(os.path.exists(yd.FFMPEG_EXE))
        print("yt-dlp and ffmpeg presence confirmed (mocked).")

    @mock.patch("yt_downloader.run_yt_dlp")
    def test_2_download_and_convert_mocked(self, mock_run):
        """
        Mock run_yt_dlp so no real download happens.
        Simulate an MP3 file being created.
        """
        print("\nRunning fully mocked yt-dlp download test...")

        # Simulate MP3 creation
        fake_mp3_path = os.path.join(yd.DOWNLOAD_DIR, "fake_song.mp3")
        with open(fake_mp3_path, "w") as f:
            f.write("fake mp3 content")

        # Call the mocked function
        yd.run_yt_dlp(self.TEST_URL)
        mock_run.assert_called_once_with(self.TEST_URL)
        print("run_yt_dlp called (mocked).")

        # Check that the fake MP3 exists
        mp3_files = glob.glob(os.path.join(yd.DOWNLOAD_DIR, "*.mp3"))
        self.assertTrue(mp3_files, "No MP3 file found")
        print(f"MP3 created (mocked): {os.path.basename(mp3_files[0])}")

        # Cleanup
        os.remove(fake_mp3_path)
        print(f"Removed fake MP3: {os.path.basename(fake_mp3_path)}")

    @classmethod
    def tearDownClass(cls):
        """Clean up fake tools"""
        if os.path.exists(yd.YTDLP_EXE):
            os.remove(yd.YTDLP_EXE)
        if os.path.exists(yd.FFMPEG_EXE):
            os.remove(yd.FFMPEG_EXE)
        print("\nAll mocked tests completed.\n")


if __name__ == "__main__":
    unittest.main(verbosity=2)
