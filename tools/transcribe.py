"""Transcribe audio/vídeo con Whisper (faster-whisper) y genera subtítulos.

Salida en media/captions/<nombre>.json con el tipo `Caption` de @remotion/captions
(una entrada por palabra) y <nombre>.srt.

Uso:
  tools/.venv/bin/python tools/transcribe.py media/raw/video.mp4 [--model small] [--language es]
"""
import argparse
import json
from pathlib import Path

from faster_whisper import WhisperModel

ROOT = Path(__file__).resolve().parent.parent


def srt_time(sec: float) -> str:
    ms = int(round(sec * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("input", type=Path)
    p.add_argument("--model", default="small", help="tiny, base, small, medium, large-v3")
    p.add_argument("--language", default=None, help="es, en... (auto si se omite)")
    p.add_argument("--out", type=Path, default=ROOT / "media" / "captions")
    a = p.parse_args()

    model = WhisperModel(a.model, device="auto", compute_type="int8")
    segments, info = model.transcribe(str(a.input), language=a.language, word_timestamps=True, vad_filter=True)
    print(f"Idioma: {info.language} ({info.language_probability:.0%})")

    captions, srt = [], []
    for i, seg in enumerate(segments, 1):
        srt.append(f"{i}\n{srt_time(seg.start)} --> {srt_time(seg.end)}\n{seg.text.strip()}\n")
        for w in seg.words or []:
            captions.append({
                "text": w.word,  # incluye el espacio inicial, como espera createTikTokStyleCaptions
                "startMs": round(w.start * 1000),
                "endMs": round(w.end * 1000),
                "timestampMs": round((w.start + w.end) / 2 * 1000),
                "confidence": round(w.probability, 3),
            })

    a.out.mkdir(parents=True, exist_ok=True)
    stem = a.input.stem
    (a.out / f"{stem}.json").write_text(json.dumps(captions, ensure_ascii=False, indent=2))
    (a.out / f"{stem}.srt").write_text("\n".join(srt))
    print(f"✓ {a.out / (stem + '.json')}  ({len(captions)} palabras)")
    print(f"✓ {a.out / (stem + '.srt')}")


if __name__ == "__main__":
    main()
