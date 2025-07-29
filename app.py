# app.py (Definitive, Final Version)

import gradio as gr
import os
import shutil

# Importing custom modules
from src.audio_processor import AudioProcessor
from src.transcriber import Transcriber
from src.translator import Translator
from src.subtitle_generator import SubtitleGenerator
from src.analyzer import Analyzer

# --- Model Initialization (No changes) ---
print("Initializing all models, please wait...")
audio_processor = AudioProcessor()
transcriber = Transcriber(model_size="base")
translator = Translator()
subtitle_generator = SubtitleGenerator()
analyzer = Analyzer()
print("\nAll models initialized. The application is ready.")

# --- USAGE COUNTER (FILLED IN) ---
# This section was previously a placeholder.
COUNTER_FILE = "usage_count.txt"
def get_usage_count():
    if not os.path.exists(COUNTER_FILE): return 0
    with open(COUNTER_FILE, "r") as f:
        try: return int(f.read().strip())
        except (ValueError, TypeError): return 0

def increment_usage_count():
    count = get_usage_count() + 1
    with open(COUNTER_FILE, "w") as f: f.write(str(count))
    return count


# --- MAIN PROCESSING FUNCTION (SIMPLIFIED) ---
def generate_subtitles_for_video(video_upload_path, apply_noise_reduction, target_language, preserve_technical_terms, quick_process, progress=gr.Progress()):
    # Simplified input validation
    if not video_upload_path:
        raise gr.Error("Error: Please upload a video file to begin.")

    temp_files_to_clean = []
    try:
        duration_limit = 60 if quick_process else None
        
        progress(0.1, desc="Step 1/5: Preparing Audio...")
        # Simplified logic: always use the uploaded file
        processed_audio_path = audio_processor.process_video_or_audio(video_upload_path, apply_noise_reduction, duration_limit)
        temp_files_to_clean.append(processed_audio_path)
        
        if not os.path.exists(processed_audio_path) or os.path.getsize(processed_audio_path) < 1024:
            raise gr.Error("Failed to extract valid audio. The source might be silent or invalid.")

        # --- The rest of the pipeline remains the same ---
        progress(0.3, desc="Step 2/5: Transcribing audio...")
        original_segments, src_lang = transcriber.transcribe_audio(processed_audio_path)
        
        progress(0.6, desc="Step 3/5: Analyzing content...")
        full_transcript_text = analyzer.get_full_text_from_segments(original_segments)
        summary = analyzer.summarize_text(full_transcript_text)
        keywords = analyzer.extract_keywords(full_transcript_text)

        original_srt_path = subtitle_generator.create_srt_file(f"subtitles_{src_lang}", original_segments)
        output_files = [original_srt_path]
        final_video_subtitle_path = original_srt_path
        
        if target_language and target_language != src_lang:
            progress(0.8, desc=f"Step 4/5: Translating to {target_language.upper()}...")
            translated_segments = translator.translate_segments(original_segments, src_lang, target_language, preserve_technical_terms)
            translated_srt_path = subtitle_generator.create_srt_file(f"subtitles_{target_language}", translated_segments)
            output_files.append(translated_srt_path)
            final_video_subtitle_path = translated_srt_path
        
        progress(1.0, desc="Step 5/5: Finalizing...")
        
        processing_summary = (f"Source Language Detected: {src_lang.upper()}\n" + f"Translation Language: {target_language.upper() if target_language else 'N/A'}")
        preview_text = full_transcript_text
        video_player_update = (video_upload_path, final_video_subtitle_path)

        return video_player_update, output_files, processing_summary, preview_text, summary, keywords

    except Exception as e:
        print(f"An error occurred in the main pipeline: {e}")
        error_message = f"An unexpected error occurred: {str(e)}"
        if isinstance(e, gr.Error) or isinstance(e, IOError):
            error_message = str(e)
        raise gr.Error(error_message)
    finally:
        for path in temp_files_to_clean:
            if os.path.exists(path):
                try:
                    if os.path.isdir(path): shutil.rmtree(path)
                    else: os.remove(path)
                except OSError as e_os: print(f"Error cleaning up file/dir {path}: {e_os}")


# --- GRADIO UI (SIMPLIFIED) ---
with gr.Blocks(theme=gr.themes.Soft(), title="Global Sound 🌍", css="style.css") as demo:
    gr.Markdown("# Global Sound — AI Video Intelligence Platform")
    gr.Markdown("Transcribe, translate, summarize, and extract keywords from your video files.")
    
    # ... (Performance note can stay the same) ...
    
    with gr.Row(equal_height=False):
        with gr.Column(scale=2):
            gr.Markdown("### 1. Input & Options")
            
            # --- REMOVED TABS, SIMPLIFIED TO UPLOAD-ONLY ---
            video_upload_input = gr.Video(label="Upload Your Video", sources=['upload'])

            with gr.Accordion("Settings", open=True):
                # ... (settings checkboxes can stay the same) ...
            
            language_dropdown = gr.Dropdown(...) # (dropdown can stay the same)
            
            with gr.Row():
                process_btn = gr.Button("Generate Insights", variant="primary", scale=3)
                stop_btn = gr.Button("Stop", variant="stop", scale=1)

        with gr.Column(scale=3):
            # ... (Results section can stay the same) ...

    process_event = process_btn.click(
        fn=generate_subtitles_for_video,
        # --- SIMPLIFIED INPUTS ---
        inputs=[video_upload_input, noise_reduction, language_dropdown, preserve_technical, quick_process_checkbox],
        outputs=[video_output, output_files, processing_details_output, preview_text, summary_output, keywords_output]
    )

    stop_btn.click(fn=None, inputs=None, outputs=None, cancels=[process_event])


    # --- Footer (FILLED IN) ---
    gr.Markdown("---")
    
    gr.Markdown(
        "### For Developers & Power Users\n"
        "This online demo is limited by the free CPU hardware. For faster performance, no time limits, and to process longer videos, you can run this application on your own machine.\n\n"
        "**Feel free to fork the repository on GitHub and run it locally, especially if you have a computer with a GPU.**\n\n"
        "➡️ **[Find the code on GitHub](https://github.com/VinodAnbalagan/global_sound_evolution)**" 
    )

    gr.Markdown("---")
    gr.Markdown("Made with ❤️ using `faster-whisper`, `mBART-50`, `T5-small`, and Gradio.")

if __name__ == "__main__":
    demo.launch(debug=True)
