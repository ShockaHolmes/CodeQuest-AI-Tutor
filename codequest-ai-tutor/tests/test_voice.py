from urllib import error

from app import voice


def test_synthesize_speech_handles_timeout(monkeypatch):
    monkeypatch.setenv("ELEVENLABS_API_KEY", "fake-key")

    def mock_urlopen(*args, **kwargs):
        raise TimeoutError("timed out")

    monkeypatch.setattr(voice.request, "urlopen", mock_urlopen)

    result = voice.synthesize_speech("Read this question")

    assert result.audio_bytes is None
    assert result.error_message is not None
    assert "Unable to connect to ElevenLabs" in result.error_message


def test_synthesize_speech_handles_connection_reset(monkeypatch):
    monkeypatch.setenv("ELEVENLABS_API_KEY", "fake-key")

    def mock_urlopen(*args, **kwargs):
        raise ConnectionResetError("connection reset by peer")

    monkeypatch.setattr(voice.request, "urlopen", mock_urlopen)

    result = voice.synthesize_speech("Read this question")

    assert result.audio_bytes is None
    assert result.error_message is not None
    assert "Unable to connect to ElevenLabs" in result.error_message


def test_synthesize_speech_handles_http_error_without_crashing(monkeypatch):
    monkeypatch.setenv("ELEVENLABS_API_KEY", "fake-key")

    def mock_urlopen(*args, **kwargs):
        raise error.HTTPError(
            url="https://api.elevenlabs.io/v1/text-to-speech/test",
            code=401,
            msg="Unauthorized",
            hdrs=None,
            fp=None,
        )

    monkeypatch.setattr(voice.request, "urlopen", mock_urlopen)

    result = voice.synthesize_speech("Read this question")

    assert result.audio_bytes is None
    assert result.error_message is not None
    assert "ElevenLabs request failed (401)." in result.error_message
