# global_sound_evolution
global sound 2.0
# Global Sound Evolution — The Creator's AI Content Suite

[![Made with Gradio](https://img.shields.io/badge/Made%20with-Gradio-orange)](https://gradio.app/)
[![Powered by Hugging Face](https://img.shields.io/badge/🤗-Powered%20by%20Hugging%20Face-yellow.svg)](https://huggingface.co/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/)

**Go beyond translation. Transcribe, translate, summarize, and extract key insights from any video on your computer.**

Turn your raw video files into ready-to-use content. Generate accurate transcripts, multilingual subtitles, concise summaries, and key topics in minutes.

This tool was built for creators, researchers, and professionals who work with video. If you've ever recorded a lecture, a user interview, or a podcast, you know the recording is just the first step. Global Sound automates the tedious work of transcribing, translating, and analyzing your content, saving you hours of manual effort.

➡️ **[Try the Live Demo on Hugging Face!](https://huggingface.co/spaces/vinod-anbalagan/Global_Sound_Evolution)** 

---

## ✨ Key Features

- **Accurate Transcription**: Powered by faster-whisper, an optimized version of OpenAI's Whisper, it generates clear text with timestamps, even from videos with background noise.
- **Intelligent Translation**: Utilizes the mBART-50 model to translate text into dozens of languages while preserving critical context.
- **AI-Generated Summaries**: Uses the T5-small model to create a concise summary of your video's content, perfect for descriptions or internal reports.
- **Automatic Keyword Extraction**: Identifies and lists the most important terms and concepts discussed in the video using the lightweight YAKE library.
- **Technical Term Preservation**: A custom mechanism ensures that jargon and acronyms (GAN, LSTM, PyTorch) are not mistranslated.
- **Downloadable Subtitles**: Generates industry-standard .srt files for both the original transcription and the translated version

---

## 🚀 How It Works

The application follows a robust, multi-stage pipeline to transform a video source into a full suite of insights.

1. **Video Upload & Audio Extraction**: The user uploads a video file. The application uses moviepy to extract the audio stream and noisereduce to clean it.
2. **Transcription**: The clean audio is fed into the faster-whisper model for highly accurate speech-to-text conversion.
3. **Content Analysis**: The full transcript is passed to the T5-small model for summarization and the YAKE algorithm for keyword extraction.
4. **Translation**: If requested, the transcribed text segments are translated by the mBART-50 model, using the custom term-protection logic.
5. **Output Generation**: The app generates downloadable .srt files and populates the user interface with the summary, keywords, and full transcript.
---

## 🛠️ Tech Stack

-   **Backend**: Python
-   **ML Models**: `faster-whisper` (Transcription), `mBART-50` (Translation), `T5-small` (Summarization)
-   **Framework**: Gradio
-   **Core Libraries**:  `moviepy`, `noisereduce`, `transformers`, `torch`, `yake`, `libsora`
-   **Deployment**: Hugging Face Spaces

---
### Project Evolution and Dependancy changes
This project's journey is a real-world story of adapting to technical constraints.

My initial vision included a feature to process videos directly from YouTube URLs. However, upon deployment to the Hugging Face cloud platform, I encountered a critical and unresolvable dependency conflict. The gradio web framework and the yt-dlp library required mutually exclusive versions of a core networking package (websockets), making it impossible for them to coexist in the same environment.

Faced with this, I made a strategic engineering decision: prioritize a stable, reliable, and valuable application over a single, blocked feature.

The result is a more focused and robust platform dedicated to processing local video files—a critical workflow for content creators, researchers, and professionals. This journey was a powerful lesson in pragmatism and the importance of adapting a product's design to overcome real-world development constraints.

---
## 🏃‍♀️ Running Locally

This online demo runs on a free CPU, which can be slow. For faster performance and no time limits, you can run this application on your own machine, especially if you have a GPU.

**1. Clone the repository:**

git clone [https://github.com/VinodAnbalagan/global-sound.git
cd global-sound](https://github.com/VinodAnbalagan/global_sound_evolution)

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

