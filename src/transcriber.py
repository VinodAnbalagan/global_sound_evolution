# src/transcriber.py

from faster_whisper import WhisperModel
import os

class Transcriber:
    def __init__(self, model_size="base"):
        """
        Initializes the Transcriber with a specific model size.
        
        Args:
            model_size (str): The size of the Whisper model to use 
                              (e.g., "tiny", "base", "small", "medium").
                              "base" is a good balance for CPU.
        """
        # Using a GPU-ready model but it will automatically fall back to CPU if no CUDA is available.
        # For Hugging Face free tier, this will be CPU.
        # We can also specify compute_type="int8" for more speed on CPU.
        self.model_size = model_size
        print(f"Loading Whisper model: {self.model_size}...")
        try:
            self.model = WhisperModel(self.model_size, device="cpu", compute_type="int8")
            print("Whisper model loaded successfully on CPU.")
        except Exception as e:
            print(f"Error loading Whisper model: {e}")
            raise

    def transcribe_audio(self, audio_path):
        """
        Transcribes the given audio file into text segments with timestamps.

        Args:
            audio_path (str): The path to the audio file to transcribe.

        Returns:
            tuple: A tuple containing:
                - list: A list of segment dictionaries with 'start', 'end', and 'text'.
                - str: The detected language code (e.g., 'en', 'es').
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found at {audio_path}")

        print(f"Starting transcription for: {audio_path}")
        try:
            # The 'vad_filter=True' argument helps remove long silent parts, improving speed and accuracy.
            segments, info = self.model.transcribe(audio_path, beam_size=5, vad_filter=True)
            
            print(f"Detected language '{info.language}' with probability {info.language_probability}")

            # faster-whisper returns a generator, so we convert it to a list of dicts
            # to match the structure we need.
            segment_list = []
            for segment in segments:
                segment_list.append({
                    "start": segment.start,
                    "end": segment.end,
                    "text": segment.text.strip()
                })
            
            print("Transcription completed.")
            return segment_list, info.language

        except Exception as e:
            print(f"An error occurred during transcription: {e}")
            # Re-raise the exception to be caught by the main app's error handler
            raise e
