from faster_whisper import WhisperModel
from config import WHISPER_MODEL_SIZE, WHISPER_DEVICE, WHISPER_COMPUTE_TYPE, WHISPER_LANGUAGE

_model: WhisperModel | None = None


def _get_model() -> WhisperModel:
    global _model
    if _model is None:
        print(f"[Transcription] Загрузка модели Whisper '{WHISPER_MODEL_SIZE}'...")
        _model = WhisperModel(
            WHISPER_MODEL_SIZE,
            device=WHISPER_DEVICE,
            compute_type=WHISPER_COMPUTE_TYPE,
        )
        print("[Transcription] Модель загружена.")
    return _model


def transcribe(audio_path: str) -> str:
    """Транскрибирует аудиофайл, возвращает текст."""
    model = _get_model()
    segments, info = model.transcribe(
        audio_path,
        beam_size=5,
        language=WHISPER_LANGUAGE,
    )
    text = " ".join(seg.text.strip() for seg in segments)
    detected = info.language if WHISPER_LANGUAGE is None else WHISPER_LANGUAGE
    print(f"[Transcription] Язык: {detected}, длина: {info.duration:.1f}с")
    return text.strip()
