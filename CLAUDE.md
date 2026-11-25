# AI-VIDEO

Repo de edición de vídeo con 5 herramientas. Lee `README.md` para estructura y comandos.

- **Remotion** (`remotion/`): carga primero la skill `remotion-best-practices`.
- **HyperFrames** (`hyperframes/`): carga primero la skill `hyperframes`; ver `hyperframes/CLAUDE.md`.
- **yt-dlp**: `tools/download.sh <URL>` → `media/raw/`.
- **FFmpeg**: binario del sistema; deja los resultados en `media/`.
- **Whisper**: `tools/.venv/bin/python tools/transcribe.py <archivo>` → `media/captions/*.json` (tipo `Caption` de Remotion) y `.srt`.

Reglas:
- Todo archivo multimedia va en `media/` (está en `.gitignore`); los assets que un proyecto necesite en render se copian a `remotion/public/` o `hyperframes/assets/`.
- Cada proyecto Node es independiente: ejecuta npm/npx dentro de su carpeta.
- Renders finales en `media/renders/`.
