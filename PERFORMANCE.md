# ⚡ Music Transcriber - Performance Optimization

## Why It's Slow

### 1. **Model Downloads on First Run** (10+ minutes)
- Demucs: 320MB (4 models)
- Qwen ASR: Fails (can't reach HuggingFace)
- Transformers/PyAnnote: 500MB+

**Solution**: Pre-cached in Docker (only first run slow)

### 2. **CPU-only Inference** (No GPU)
- Each step runs on CPU
- Demucs source separation: 2-3 minutes per song
- Qwen ASR: 5+ minutes per song

**Solution**: Disable slow features or use GPU

### 3. **All Features Enabled**
- Demucs separation (SLOW)
- Qwen ASR transcription (SLOW)
- Easytranscriber (SLOW)
- These are optional but enabled by default

**Solution**: Disable optional features

---

## 🚀 Fast Configuration

### Option 1: Fastest (Core Features Only)

Edit `.env`:
```env
DEMUCS_ENABLED=false
QWEN_ASR_ENABLED=false
EASYTRANSCRIBER_ENABLED=false
```

**Processing Time**: 30-60 seconds per song
**Features**: Raga, Tala, Pitch, Tonic

### Option 2: Medium Speed (+ Source Separation)

```env
DEMUCS_ENABLED=true
QWEN_ASR_ENABLED=false
EASYTRANSCRIBER_ENABLED=false
```

**Processing Time**: 2-3 minutes per song
**Features**: + Audio stems (vocals, drums, bass, etc.)

### Option 3: Full Features (Slow)

```env
DEMUCS_ENABLED=true
QWEN_ASR_ENABLED=true
EASYTRANSCRIBER_ENABLED=true
```

**Processing Time**: 5-10 minutes per song
**Features**: + Song lyrics + Word timestamps

---

## 💾 Optimization Changes Made

### 1. **Lazy Model Loading**
- Models only load when first used
- Saves startup time
- Avoids unnecessary memory

### 2. **Configurable Features**
- Disable slow features via .env
- Don't run if not needed

### 3. **Error Handling**
- Skip failed steps, continue processing
- Don't crash on instrument classification failure

### 4. **File Cleanup**
- Uploaded files deleted after processing
- Saves disk space

### 5. **Audio Truncation**
- Limit to 5 minutes max
- Prevents extremely long processing

### 6. **Error Messages**
- Better logging
- Know what's slow

---

## 🔧 How to Enable (Create .env file)

1. **Copy template**
   ```bash
   cp .env.example .env
   ```

2. **Edit .env** and set:
   ```env
   # Fastest: disable everything except core
   DEMUCS_ENABLED=false
   QWEN_ASR_ENABLED=false
   
   # Or medium: keep separation
   DEMUCS_ENABLED=true
   QWEN_ASR_ENABLED=false
   ```

3. **Restart Docker**
   ```bash
   docker-compose down
   docker-compose up
   ```

---

## 📊 Speed Comparison

| Configuration | Time | Features |
|---|---|---|
| **Core Only** | 30-60 sec | Raga, Tala, Pitch |
| **+ Separation** | 2-3 min | + Stems |
| **+ ASR** | 5-10 min | + Lyrics |
| **All** | 10-15 min | All features |

---

## 🎯 Recommended Setup

### **For Users** (Fast)
```env
DEMUCS_ENABLED=false
QWEN_ASR_ENABLED=false
```
Result: 30-60 seconds, core analysis only

### **For Musicians** (Medium)
```env
DEMUCS_ENABLED=true
QWEN_ASR_ENABLED=false
```
Result: 2-3 minutes, with source separation

### **For Full Analysis** (Slow but Complete)
```env
DEMUCS_ENABLED=true
QWEN_ASR_ENABLED=true
```
Result: 5-10 minutes, everything

---

## 🖥️ Using GPU (Much Faster)

If you have NVIDIA GPU:

1. **Install CUDA & cuDNN**
   - Download: https://developer.nvidia.com/cuda-toolkit

2. **Update Docker Compose**
   ```yaml
   services:
     app:
       image: nvidia/cuda:12.2-cudnn8-runtime-ubuntu22.04
       runtime: nvidia
       environment:
         - NVIDIA_VISIBLE_DEVICES=all
   ```

3. **Update .env**
   ```env
   USE_GPU=true
   ```

4. **Restart**
   ```bash
   docker-compose down
   docker-compose up
   ```

**Speed with GPU**: 10-30x faster!

---

## 📝 Configuration File (.env.example)

```env
# Production
SECRET_KEY=your-secret-key

# Model settings
MODEL_CACHE_DIR=./data/models
TARGET_SAMPLE_RATE=22050

# Feature toggles (OPTIMIZATION)
DEMUCS_ENABLED=false          # Source separation (slow)
QWEN_ASR_ENABLED=false        # Lyrics transcription (very slow)
EASYTRANSCRIBER_ENABLED=false # Alignment (slow)

# GPU acceleration
USE_GPU=false                  # Enable if NVIDIA GPU available
DEMUCS_MODEL=htdemucs_ft       # Model quality

# Server
HOST=0.0.0.0
PORT=5000
MAX_AUDIO_LENGTH=300          # Max 5 minutes
```

---

## 🚀 Restart Steps

```bash
# 1. Stop current container
docker-compose down

# 2. Create/edit .env
nano .env  # or use text editor

# 3. Restart with new config
docker-compose up
```

Changes take effect immediately.

---

## ⚠️ Common Issues & Fixes

### **Upload Takes 5+ Minutes**
→ Demucs separation running
→ Set `DEMUCS_ENABLED=false` in .env

### **"Qwen ASR" Failed**
→ Network issue (can't reach HuggingFace)
→ Already handled - graceful degradation

### **App Very Slow on First Request**
→ Models downloading/loading
→ Wait 5-10 minutes first time
→ Subsequent requests much faster

### **Memory Running Out**
→ Demucs + Qwen both running
→ Disable one in .env
→ Or increase Docker memory limit

---

## 💡 Pro Tips

1. **Test Features Individually**
   - Disable all first
   - Enable one at a time
   - See which is slow

2. **Monitor Logs**
   ```bash
   docker logs -f music-transcriber
   ```
   Shows what step is running

3. **Use Small Files First**
   - 10-30 second clips
   - Quick feedback
   - Find bottleneck

4. **Cache Models**
   - First run slow (downloads)
   - Subsequent runs faster
   - Models cached in `data/models/`

---

## 📈 Expected Times (CPU)

| Step | Time |
|------|------|
| Load audio | 1 sec |
| Detect tonic | 2 sec |
| Extract pitch | 5 sec |
| Generate sargam | 1 sec |
| Identify raga | 2 sec |
| Detect tala | 5 sec |
| Classify instruments | 5 sec |
| **Separate sources** | 120 sec ⭐ SLOW |
| **Transcribe lyrics** | 300 sec ⭐ VERY SLOW |
| Visualize | 2 sec |
| **TOTAL (Core)** | **~30 sec** |
| **+ Separation** | **~150 sec** |
| **+ ASR** | **~450 sec** |

---

## ✅ Quick Fix Checklist

- [ ] Created .env file
- [ ] Set DEMUCS_ENABLED=false
- [ ] Set QWEN_ASR_ENABLED=false
- [ ] Restarted docker-compose
- [ ] Tested with small audio file
- [ ] Confirmed faster speed

Expected result: **30-60 seconds per song** (core analysis)

Done! 🎵
