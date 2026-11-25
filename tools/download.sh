#!/usr/bin/env bash
# Descarga un vídeo con yt-dlp a media/raw/ (MP4).
# Uso: tools/download.sh <URL> [args extra de yt-dlp]
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
URL="${1:?Uso: tools/download.sh <URL>}"; shift || true
"$ROOT/tools/.venv/bin/yt-dlp" \
  -f "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/b" --merge-output-format mp4 \
  -o "$ROOT/media/raw/%(title).80B [%(id)s].%(ext)s" \
  "$@" "$URL"
