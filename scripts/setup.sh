#!/usr/bin/env bash
# Instala las 5 herramientas: Remotion, HyperFrames, yt-dlp, FFmpeg y Whisper.
set -euo pipefail
cd "$(dirname "$0")/.."

# FFmpeg (sistema)
if ! command -v ffmpeg >/dev/null; then
  if command -v brew >/dev/null; then brew install ffmpeg
  elif command -v apt-get >/dev/null; then sudo apt-get update && sudo apt-get install -y ffmpeg
  else echo "Instala FFmpeg manualmente: https://ffmpeg.org/download.html" >&2; exit 1; fi
fi

# yt-dlp + Whisper (Python, vía uv)
command -v uv >/dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh
(cd tools && uv sync)

# Remotion + HyperFrames (Node 22+)
(cd remotion && npm ci)
(cd hyperframes && npm ci)

echo "✓ Listo: remotion, hyperframes, yt-dlp, ffmpeg, whisper"
