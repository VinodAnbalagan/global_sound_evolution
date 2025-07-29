# src/subtitle_generator.py

import os
import tempfile
from datetime import timedelta

class SubtitleGenerator:
    def __init__(self):
        print("SubtitleGenerator initialized.")

    def _seconds_to_srt_time(self, seconds):
        """Converts seconds (float) to an SRT time string format HH:MM:SS,ms."""
        td = timedelta(seconds=seconds)
        minutes, seconds = divmod(td.seconds, 60)
        hours, minutes = divmod(minutes, 60)
        milliseconds = td.microseconds // 1000
        return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

    def create_srt_file(self, base_filename, segments):
        """
        Creates a .srt subtitle file from a list of transcribed/translated segments.

        Args:
            base_filename (str): The base name for the output file (e.g., "subtitles_en").
            segments (list): A list of segment dictionaries with 'start', 'end', and 'text'.

        Returns:
            str: The path to the created .srt file.
        """
        temp_dir = tempfile.gettempdir()
        srt_path = os.path.join(temp_dir, f"{base_filename}.srt")
        
        print(f"Generating SRT file at: {srt_path}")

        with open(srt_path, 'w', encoding='utf-8') as f:
            for i, segment in enumerate(segments):
                start_time = self._seconds_to_srt_time(segment['start'])
                end_time = self._seconds_to_srt_time(segment['end'])
                text = segment['text']

                f.write(f"{i + 1}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{text}\n\n")

        print("SRT file generation complete.")
        return srt_path