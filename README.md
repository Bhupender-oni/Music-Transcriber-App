# 🎵 Music Transcriber - Indian Classical Music Analysis

## Overview

A complete music transcription and analysis system for Indian classical music with support for raga identification, tala detection, pitch analysis, and source separation.

**Features**:
- ✅ Real-time music analysis (30-60 seconds per song)
- ✅ 150+ raga database with detailed information
- ✅ Automatic raga identification
- ✅ Pitch extraction & visualization
- ✅ Tala (rhythm) detection
- ✅ Instrument classification
- ✅ Source separation
- ✅ Comprehensive musical analysis tools

---

## Quick Start

### Option 1: Web App (Immediate)
```bash
Open: http://localhost:5000
Upload audio → Get analysis
```

### Option 2: Desktop App (10-15 min)
```bash
# Windows
build-desktop.bat

# macOS/Linux
./build-desktop.sh
```

### Option 3: Mobile App (15-20 min)
```bash
# Android
build-mobile.bat android

# iOS (macOS only)
./build-mobile.sh ios
```

---

## Requirements

- Docker & Docker Compose
- Node.js 18+ (for desktop/mobile builds)
- Python 3.11+ (for local development)

---

## Project Structure

```
Music-Transcriber-App/
├── src/                    # Core application
│   ├── api/               # Flask routes & WebSocket
│   ├── audio/             # Audio processing
│   ├── models/            # ML models (Raga, Tala, etc.)
│   ├── transcription/     # Music transcription
│   ├── separation/        # Source separation
│   ├── visualization/     # Charts & plots
│   ├── config.py          # Configuration
│   └── music_analysis_tools.py  # Analysis tools (10 tools)
├── data/                   # Databases
│   ├── raga_database.json (original, 79 ragas)
│   ├── raga_database_extended.json (150+ ragas)
│   └── instrument_profiles.json (95+ instruments)
├── web/                    # Web UI
│   ├── templates/         # HTML
│   ├── static/            # CSS/JavaScript
├── tests/                 # Test suite
├── docker-compose.yml     # Docker configuration
├── Dockerfile             # Image definition
├── run.py                 # Application entry point
├── requirements.txt       # Python dependencies
└── pyproject.toml         # Project metadata
```

---

## Running the App

### Docker (Recommended)
```bash
docker-compose up
# Access at: http://localhost:5000
```

### Local Development
```bash
pip install -e .
python run.py
```

---

## Build Instructions

See `PERFORMANCE.md` and `MUSICAL_TOOLS_GUIDE.md` for detailed guides.

### Desktop Build
```bash
build-desktop.bat        # Windows
./build-desktop.sh       # macOS/Linux
```

### Mobile Build
```bash
build-mobile.bat android # Android
./build-mobile.sh ios    # iOS (macOS only)
```

---

## Features

### Music Analysis
- **Raga Identification** - Identifies 150+ ragas with confidence scores
- **Pitch Detection** - Extracts F0 contour using librosa.pyin
- **Tala Detection** - Detects rhythmic patterns
- **Sargam Generation** - Converts pitch to Indian note sequence
- **Ornamentation Detection** - Identifies Meend, Gamak, Khatka, etc.
- **Instrument Classification** - Classifies 95+ instruments

### Advanced Tools (10 Analysis Tools)
1. Raga characteristics analysis
2. Note frequency analysis
3. Ornamentation detection
4. Time appropriateness checking
5. Instrument suitability
6. Raga structure analysis
7. Mood analysis
8. Raga comparison
9. Tala analysis
10. Database search & filtering

### Databases
- **150+ Ragas** with complete musical details
- **95+ Instruments** with frequency profiles
- **10 Thaat Systems** (parent scales)
- **Hindustani & Carnatic** variants

---

## Performance

- **Processing Time**: 30-60 seconds per song (optimized)
- **Features**: Lazy loading, configurable analysis
- **Optimization**: `.env` file for feature toggles
- **Database**: 40+ KB of comprehensive music information

---

## Documentation

- **PERFORMANCE.md** - Performance optimization guide
- **MUSICAL_TOOLS_GUIDE.md** - Complete analysis tools documentation
- **README.md** - This file

---

## Technology Stack

### Backend
- Flask (REST API)
- librosa (audio processing)
- numpy/scipy (signal processing)
- torch/demucs (source separation)
- plotly (visualization)

### Frontend
- HTML5 / CSS3
- jQuery
- Plotly.js

### Deployment
- Docker
- Python 3.11
- Linux/Windows/macOS

---

## Configuration

Edit `.env` to configure:
```env
# Feature toggles (disable for faster processing)
DEMUCS_ENABLED=false        # Source separation
QWEN_ASR_ENABLED=false      # Lyrics transcription

# Model settings
MODEL_CACHE_DIR=./data/models
TARGET_SAMPLE_RATE=22050
MAX_AUDIO_LENGTH=300        # 5 minutes max
```

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web UI |
| `/upload` | POST | Upload audio file |
| `/status/<job_id>` | GET | Check processing status |

---

## Testing

Run test suite:
```bash
pytest tests/
```

Includes tests for:
- Audio processing
- Raga identification
- Source separation

---

## Integration

### For Web App
Music analysis tools are built into the processing pipeline automatically.

### For Custom Integration
```python
from src.music_analysis_tools import MusicalTools, RagaMusicDatabase

tools = MusicalTools()
db = RagaMusicDatabase.load_extended_database()

# Identify raga from notes
matches = tools.identify_raga_from_notes(['S', 'R', 'G', 'M#', 'P', 'D', 'N'])

# Search by time
evening_ragas = RagaMusicDatabase.search_ragas_by_time('Evening')

# Get learning progression
progression = RagaMusicDatabase.get_raga_difficulty_progression()
```

---

## License

Open source - See LICENSE file

---

## Support

- Check `MUSICAL_TOOLS_GUIDE.md` for tool documentation
- Check `PERFORMANCE.md` for optimization options
- Review `docker-compose.yml` for deployment configuration

---

## Status

✅ **Production Ready**
- Web app: Running
- Desktop: Ready to build
- Mobile: Ready to build
- 150+ ragas: Complete
- 10 analysis tools: Functional
- Comprehensive documentation: Included

---

**Built with ❤️ for Indian classical music** 🎵
