# Music Transcriber 2026

A comprehensive Indian music transcription system with:
- 🎵 Tonic (Sa) detection
- 🎼 Sargam generation with ornament markers (meend, gamak, etc.)
- 🎸 Raga identification (50+ ragas, ensemble method)
- 🥁 Tala detection (rhythm cycle identification)
- 🎤 Instrument classification (spectral matching)
- 🔉 Source separation (Demucs 4.0+, CPU‑compatible)
- 📝 Lyrics transcription (Qwen3‑ASR integration, optional)
- 📈 Interactive visualizations (Plotly 5.25+)

## Installation

```bash
# Clone or create project folder
cd music-transcriber-2026

# Create virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate    # Mac/Linux

# Install in editable mode
pip install -e .[dev]