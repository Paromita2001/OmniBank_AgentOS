import whisper
import os
import tempfile
import subprocess
import uuid
from functools import lru_cache


# -----------------------------------
# Load Whisper Model (Cached)
# -----------------------------------
@lru_cache(maxsize=1)
def load_model():
    return whisper.load_model("tiny")  # CPU safe


# -----------------------------------
# Convert Audio to 16kHz Mono WAV
# -----------------------------------
def convert_to_wav(input_path: str) -> str:
    temp_dir = tempfile.gettempdir()
    output_path = os.path.join(temp_dir, f"{uuid.uuid4().hex}.wav")

    cmd = [
        "ffmpeg",
        "-y",
        "-i", input_path,
        "-ar", "16000",
        "-ac", "1",
        output_path
    ]

    subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if not os.path.exists(output_path):
        raise RuntimeError("Audio conversion failed")

    return output_path


# -----------------------------------
# Main STT Function
# -----------------------------------
def speech_to_text(audio_path: str) -> str:

    if not audio_path or not os.path.exists(audio_path):
        return ""

    model = load_model()

    try:
        safe_wav = convert_to_wav(audio_path)

        result = model.transcribe(
            safe_wav,
            language="en",
            fp16=False,
            temperature=0.0
        )

        text = result.get("text", "").strip()
        return text

    except Exception as e:
        print("STT Error:", e)
        return ""

    finally:
        try:
            if 'safe_wav' in locals() and os.path.exists(safe_wav):
                os.remove(safe_wav)
        except:
            pass