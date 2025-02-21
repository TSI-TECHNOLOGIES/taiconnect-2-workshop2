import whisper
from gtts import gTTS
from audio import whispher_model


def speech_to_text(audio_file_path: str):
    model = whispher_model
    transcript = model.transcribe(audio_file_path, language="en")
    return transcript["text"]

def text_to_speech(text: str, audio_file_path: str):
    tts = gTTS(text=text, lang="en")
    tts.save(audio_file_path)
    return audio_file_path