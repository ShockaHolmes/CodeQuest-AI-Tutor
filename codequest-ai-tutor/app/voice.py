from __future__ import annotations

import json
import os
import socket
from dataclasses import dataclass
from urllib import error, request

DEFAULT_ELEVENLABS_VOICE_ID = "kdmDKE6EkgrWrrykO9Qt"
DEFAULT_ELEVENLABS_MODEL_ID = "eleven_multilingual_v2"
ELEVENLABS_API_ROOT = "https://api.elevenlabs.io/v1/text-to-speech"


@dataclass
class VoiceResult:
    audio_bytes: bytes | None = None
    error_message: str | None = None


def has_elevenlabs_key() -> bool:
    """Return True when a valid ElevenLabs API key is available."""
    return bool(os.getenv("ELEVENLABS_API_KEY", "").strip())


def synthesize_speech(
    text: str,
    *,
    voice_id: str | None = None,
    model_id: str = DEFAULT_ELEVENLABS_MODEL_ID,
) -> VoiceResult:
    """Generate speech audio using ElevenLabs text-to-speech API."""
    api_key = os.getenv("ELEVENLABS_API_KEY", "").strip()
    if not api_key:
        return VoiceResult(error_message="Missing ELEVENLABS_API_KEY environment variable.")

    cleaned_text = text.strip()
    if not cleaned_text:
        return VoiceResult(error_message="Cannot read empty text.")

    selected_voice = (voice_id or os.getenv("ELEVENLABS_VOICE_ID", "")).strip() or DEFAULT_ELEVENLABS_VOICE_ID

    payload = {
        "text": cleaned_text,
        "model_id": model_id,
        "voice_settings": {
            "stability": 0.45,
            "similarity_boost": 0.8,
        },
    }

    api_url = f"{ELEVENLABS_API_ROOT}/{selected_voice}"
    api_request = request.Request(
        api_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        },
        method="POST",
    )

    try:
        with request.urlopen(api_request, timeout=30) as response:
            return VoiceResult(audio_bytes=response.read())
    except error.HTTPError as exc:
        details = ""
        try:
            raw_body = exc.read().decode("utf-8", errors="ignore")
            parsed = json.loads(raw_body)
            details = parsed.get("detail", {}).get("message", "")
        except (json.JSONDecodeError, AttributeError, ValueError):
            details = ""

        status_text = f"ElevenLabs request failed ({exc.code})."
        return VoiceResult(error_message=f"{status_text} {details}".strip())
    except error.URLError as exc:
        return VoiceResult(error_message=f"Unable to connect to ElevenLabs: {exc.reason}")
    except (TimeoutError, ConnectionError, ConnectionResetError, socket.timeout) as exc:
        return VoiceResult(error_message=f"Unable to connect to ElevenLabs: {exc}")
    except Exception:
        # Keep the tutor app responsive even if the TTS provider fails unexpectedly.
        return VoiceResult(error_message="Unexpected voice service error. Please try again.")
