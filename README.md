# AI-VIDEO — The Editing Engine

Cinco superpoderes para que un agente (Claude Code) edite vídeo y haga motion graphics:

| # | Herramienta | Para qué | Dónde |
|---|---|---|---|
| 1 | **Remotion** | Motion graphics con React | `remotion/` |
| 2 | **HyperFrames** | Motion graphics con HTML/CSS/GSAP | `hyperframes/` |
| 3 | **yt-dlp** | Descargar vídeos (YouTube, X, etc.) | `tools/download.sh` |
| 4 | **FFmpeg** | Cortar, convertir, unir, extraer audio | sistema (`ffmpeg`) |
| 5 | **Whisper** | Transcribir → subtítulos | `tools/transcribe.py` |

## Estructura

```
AI-VIDEO/
├── .claude/skills/      # Skills de Remotion (remotion-*) y HyperFrames
├── remotion/            # Proyecto Remotion (React)
├── hyperframes/         # Proyecto HyperFrames (HTML)
├── tools/               # Entorno Python (uv): yt-dlp + Whisper
│   ├── download.sh
│   └── transcribe.py
├── media/               # Archivos de trabajo (no se versionan)
│   ├── raw/             # descargas / material original
│   ├── audio/           # audio extraído
│   ├── captions/        # subtítulos JSON (Remotion) y SRT
│   └── renders/         # vídeos finales
└── scripts/setup.sh     # Instala todo
```

## Instalación

Requiere Node 22+ y Python 3.10+.

```bash
./scripts/setup.sh
```

## Flujo típico

```bash
# 1. Descargar
tools/download.sh "https://www.youtube.com/watch?v=..."

# 2. Recortar / extraer audio con FFmpeg
ffmpeg -ss 00:01:00 -to 00:01:30 -i "media/raw/video.mp4" -c copy media/raw/clip.mp4
ffmpeg -i media/raw/clip.mp4 -vn -ar 16000 -ac 1 media/audio/clip.wav

# 3. Transcribir con Whisper → media/captions/clip.json (+ .srt)
tools/.venv/bin/python tools/transcribe.py media/audio/clip.wav --language es

# 4a. Motion graphics con Remotion
cd remotion && npm run dev                                  # Studio
npx remotion render HelloWorld ../media/renders/out.mp4     # Render

# 4b. …o con HyperFrames
cd hyperframes && npm run dev                               # Preview
npx hyperframes render --quality looks -o ../media/renders/out.mp4
```

Los JSON de `media/captions/` usan el tipo `Caption` de `@remotion/captions`,
así que se pueden copiar a `remotion/public/` y usar directamente.
