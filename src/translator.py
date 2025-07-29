# src/translator.py

from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
import torch
import re

class Translator:
    def __init__(self, model_name="facebook/mbart-large-50-many-to-many-mmt"):
        """
        Initializes the Translator with the mBART-50 model.
        """
        # Determine device
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Initializing Translator on device: {self.device}")

        try:
            self.model = MBartForConditionalGeneration.from_pretrained(model_name).to(self.device)
            self.tokenizer = MBart50TokenizerFast.from_pretrained(model_name)
            print("Translator model and tokenizer loaded successfully.")
        except Exception as e:
            print(f"Error loading translation model/tokenizer: {e}")
            raise

    def _protect_technical_terms(self, text):
        """
        Finds technical-looking terms (all-caps, camelCase with numbers) and replaces them
        with placeholders.
        
        Returns:
            tuple: The processed text and a dictionary mapping placeholders to original terms.
        """
        # Regex to find all-caps words (like GAN, CNN), mixed-case with numbers (PyTorch1.0), etc.
        # This is a simple heuristic and can be improved.
        pattern = re.compile(r'\b([A-Z]{2,}|[A-Za-z]*[0-9]+[A-Za-z]*)\b')
        protections = {}
        count = 0

        def replace_func(match):
            nonlocal count
            term = match.group(0)
            placeholder = f"__TERM{count}__"
            protections[placeholder] = term
            count += 1
            return placeholder

        processed_text = pattern.sub(replace_func, text)
        return processed_text, protections

    def _unprotect_technical_terms(self, text, protections):
        """Replaces placeholders with their original technical terms."""
        for placeholder, original in protections.items():
            text = text.replace(placeholder, original)
        return text

    def translate_segments(self, segments, src_lang, target_lang, preserve_technical_terms):
        """
        Translates a list of text segments from a source language to a target language.

        Args:
            segments (list): A list of dictionaries with a 'text' key.
            src_lang (str): The source language code (e.g., 'en_XX').
            target_lang (str): The target language code (e.g., 'es_XX').
            preserve_technical_terms (bool): Whether to protect technical terms from translation.

        Returns:
            list: The list of segments with the 'text' key now containing translated text.
        """
        # mBART requires specific language codes
        lang_code_map = {
            'en': 'en_XX', 'es': 'es_XX', 'fr': 'fr_XX', 'de': 'de_DE', 'zh': 'zh_CN',
            'ru': 'ru_RU', 'ja': 'ja_XX', 'ar': 'ar_AR', 'hi': 'hi_IN', 'ko': 'ko_KR',
            'pt': 'pt_XX', 'ta': 'ta_IN', 'uk': 'uk_UA', 'vi': 'vi_VN'
        }
        
        # Fallback to the code itself if not in our simple map
        mbart_src_lang = lang_code_map.get(src_lang, src_lang)
        mbart_target_lang = lang_code_map.get(target_lang, target_lang)
        
        print(f"Translating from {mbart_src_lang} to {mbart_target_lang}...")

        translated_segments = []
        for i, segment in enumerate(segments):
            text_to_translate = segment['text']
            protections = {}
            
            if preserve_technical_terms:
                text_to_translate, protections = self._protect_technical_terms(text_to_translate)
            
            # Set the source language for the tokenizer
            self.tokenizer.src_lang = mbart_src_lang
            
            # Encode the text
            encoded_text = self.tokenizer(text_to_translate, return_tensors="pt").to(self.device)
            
            # Generate translation, force the output to be the target language
            generated_tokens = self.model.generate(
                **encoded_text,
                forced_bos_token_id=self.tokenizer.lang_code_to_id[mbart_target_lang]
            )
            
            # Decode the translated text
            translated_text = self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]

            if preserve_technical_terms:
                translated_text = self._unprotect_technical_terms(translated_text, protections)
                
            # Keep original start/end times, just update the text
            translated_segments.append({
                "start": segment['start'],
                "end": segment['end'],
                "text": translated_text
            })
            
            if (i + 1) % 10 == 0:
                print(f"Translated {i + 1}/{len(segments)} segments...")

        print("Translation complete.")
        return translated_segments
