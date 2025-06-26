import os
from edge_tts import Communicate
from langdetect import detect, DetectorFactory
from moviepy.editor import AudioFileClip, concatenate_audioclips
from .transliterate_uz import to_latin

DetectorFactory.seed = 0  # Стабильность в detect()


def detect_language(text):
    try:
        lang = detect(text)
        return lang if lang in ("uz", "ru", "en") else "uz"
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

    if language == "uz" and not any("\u0400" <= c <= "\u04FF" for c in text):  # узбекская латиница
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

    # Собирать в единый файл через moviepy
    try:
        clips = [AudioFileClip(f) for f in audio_files]
        final = concatenate_audioclips(clips)
        final.write_audiofile(output_path_prefix + ".mp3", codec='libmp3lame')

        for clip in clips:
            clip.close()
    except Exception as e:
        print(f"[⚠️] Ошибка при объединении аудио: {e}")
        raise

    # Удаление временных файлов
    for file in audio_files:
        try:
            os.remove(file)
        except Exception as e:
            print(f"[⚠️] Не удалось удалить временный файл {file}: {e}")
