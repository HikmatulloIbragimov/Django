import os
from edge_tts import Communicate
from pydub import AudioSegment
from langdetect import detect, DetectorFactory
from .transliterate_uz import to_latin

DetectorFactory.seed = 0  # Чтобы результаты были стабильными


def detect_language(text):
    try:
        lang = detect(text)
        if lang == "uz":
            return "uz"
        elif lang == "ru":
            return "ru"
        elif lang == "en":
            return "en"
        else:
            return "uz"  # дефолт
    except Exception:
        return "uz"


def get_voice_for_lang(lang):
    voices = {
        "ru": "ru-RU-DmitryNeural",
        "uz": "uz-UZ-MadinaNeural",
        "en": "en-US-GuyNeural"
    }
    return voices.get(lang, "en-US-GuyNeural")


async def text_to_speech_parts(text, output_path_prefix, chunk_size=2000):
    language = detect_language(text)
    voice = get_voice_for_lang(language)

    print(f"[✔] Detected language: {language}")
    print(f"[✔] Using voice: {voice}")
    print(f"[📄] Original text: {text[:100]}...")

    if language == "uz" and not any("\u0400" <= c <= "\u04FF" for c in text):  # если узбек и латиница
        processed_text = to_latin(text)
    else:
        processed_text = text

    chunks = [processed_text[i:i + chunk_size] for i in range(0, len(processed_text), chunk_size)]
    audio_files = []

    for idx, chunk in enumerate(chunks):
        if not chunk.strip():
            continue
        part_path = f"{output_path_prefix}_part{idx}.mp3"
        try:
            communicate = Communicate(text=chunk, voice=voice)
            await communicate.save(part_path)
            audio_files.append(part_path)
        except Exception as e:
            print(f"[❌] Error on chunk {idx}: {e}")

    if not audio_files:
        raise RuntimeError("❌ Не удалось озвучить ни одну часть текста!")

    combined = AudioSegment.empty()
    for file in audio_files:
        try:
            segment = AudioSegment.from_file(file)
            combined += segment + AudioSegment.silent(duration=500)
        except Exception as e:
            print(f"[⚠️] Failed to load audio file {file}: {e}")

    combined.export(output_path_prefix + ".mp3", format="mp3")

    for file in audio_files:
        try:
            os.remove(file)
        except Exception as e:
            print(f"[⚠️] Failed to delete temp file {file}: {e}")
