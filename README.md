# global_sound_evolution
global sound 2.0
# Global Sound 🌍 — AI Video Intelligence Platform

[![Made with Gradio](https://img.shields.io/badge/Made%20with-Gradio-orange)](https://gradio.app/)
[![Powered by Hugging Face](https://img.shields.io/badge/🤗-Powered%20by%20Hugging%20Face-yellow.svg)](https://huggingface.co/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/)

**Go beyond translation. Transcribe, translate, summarize, and extract key insights from any video on your computer or from YouTube.**

This tool was born from a simple desire: to make knowledge accessible. It began as a translator but has evolved into a comprehensive analysis tool. Whether you're a student trying to grasp a dense lecture, a creator repurposing content, or a professional needing to quickly understand a competitor's webinar, Global Sound saves you time and breaks down barriers.

➡️ **[Try the Live Demo on Hugging Face!](https://huggingface.co/spaces/vinod-anbalagan/Global_Sound_Evolution)** 

---

## ✨ Key Features

-   **Multi-Source Input**: Process videos by either uploading a file directly or by simply pasting a YouTube URL.
-   **Accurate Transcription**: Powered by **`faster-whisper`**, it generates clear text with timestamps, even from videos with background noise.
-   **Intelligent Translation**: Utilizes the **`mBART-50`** model to translate text into dozens of languages.
-   **AI-Generated Summaries**: Uses the **`T5-small`** model to create a concise, abstractive summary of the video's content, giving you the key points in seconds.
-   **Automatic Keyword Extraction**: Identifies and lists the most important terms and concepts discussed in the video using `YAKE`.
-   **Technical Term Preservation**: A custom mechanism ensures that jargon and acronyms (`GAN`, `LSTM`, `PyTorch`) are not mistranslated, maintaining contextual integrity.
-   **Downloadable Subtitles**: Generates standard `.srt` files for both the original transcription and the translation.

---

## 🚀 How It Works

The application follows a robust, multi-stage pipeline to transform a video source into a full suite of insights.

1.  **Input & Audio Extraction**: The app accepts a video file or YouTube URL, then uses `moviepy` or `yt-dlp` to extract a clean audio stream.
2.  **Transcription**: The audio is fed into the `faster-whisper` model for highly accurate speech-to-text conversion.
3.  **Content Analysis**:
    -   The full transcript is passed to the `T5-small` model to generate a summary.
    -   The `YAKE` algorithm extracts critical keywords from the transcript.
4.  **Translation**: If requested, the transcribed text segments are translated by the `mBART-50` model, protecting any technical terms.
5.  **Output Generation**: The app generates `.srt` files for download and populates the UI with the summary, keywords, and full transcript.

---

## 🛠️ Tech Stack

-   **Backend**: Python
-   **ML Models**: `faster-whisper` (Transcription), `mBART-50` (Translation), `T5-small` (Summarization)
-   **Framework**: Gradio
-   **Core Libraries**: `yt-dlp`, `moviepy`, `noisereduce`, `transformers`, `torch`, `yake`
-   **Deployment**: Hugging Face Spaces

---

## 🏃‍♀️ Running Locally

This online demo runs on a free CPU, which can be slow. For faster performance and no time limits, you can run this application on your own machine, especially if you have a GPU.

**1. Clone the repository:**

git clone https://github.com/VinodAnbalagan/global-sound.git
cd global-sound

**2. Create a virtual environment and install dependancies:**
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

**3. (Optional but Recommended) Install FFmpeg:**
The application uses FFmpeg for audio processing. (See previous instructions for installing FFmpeg).

**4. Launch the application:**

bash
python app.py
The application will be available at http://127.0.0.1:7860.

