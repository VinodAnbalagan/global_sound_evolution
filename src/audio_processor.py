# src/audio_processor.py (Heavily Modified)

import os
import tempfile
import yt_dlp
from moviepy.editor import VideoFileClip
import librosa
import numpy as np
import soundfile as sf
import noisereduce as nr

class AudioProcessor:
    def __init__(self):
        # You can add any model initializations here if needed in the future
        print("AudioProcessor initialized.")

    def download_audio_from_url(self, url):
        """
        Downloads the audio from a YouTube URL to a temporary mp3 file.
        Returns the path to the downloaded audio file.
        """
        temp_dir = tempfile.mkdtemp()
        options = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(temp_dir, 'downloaded_audio.%(ext)s'),
            'quiet': True,
        }
        with yt_dlp.YoutubeDL(options) as ydl:
            try:
                ydl.download([url])
            except Exception as e:
                raise IOError(f"Failed to download or process YouTube URL: {e}")
        
        # Return the path to the downloaded file
        return os.path.join(temp_dir, 'downloaded_audio.mp3')

    def process_video_or_audio(self, source_path, is_url, apply_noise_reduction, duration_limit=None):
        """
        A unified function to handle both video files and downloaded audio.
        - If it's a URL, source_path is assumed to be an audio file.
        - If it's a video upload, it extracts the audio first.
        """
        if is_url:
            # Source is already an audio file downloaded from a URL
            audio_path = source_path
        else:
            # Source is a video file, need to extract audio
            print(f"Extracting audio from video: {source_path}")
            video = VideoFileClip(source_path)
            temp_audio_path = tempfile.mktemp(suffix='.wav')
            video.audio.write_audiofile(temp_audio_path, codec='pcm_s16le')
            audio_path = temp_audio_path
        
        # Now, process the audio file (trim, noise reduce)
        print("Loading audio for processing...")
        y, sr = librosa.load(audio_path, sr=16000, mono=True)

        if duration_limit:
            y = y[:int(duration_limit * sr)]

        if apply_noise_reduction:
            print("Applying noise reduction...")
            y = nr.reduce_noise(y=y, sr=sr)
        
        processed_audio_path = tempfile.mktemp(suffix='.wav')
        sf.write(processed_audio_path, y, sr)
        
        # If the original audio was extracted from video, it's temporary and should be cleaned up
        if not is_url:
            os.remove(audio_path)
            
        return processed_audio_path