# Groq API Setup Guide

## Get Your Free Groq API Key

1. **Sign up at Groq**: https://console.groq.com/
2. **Create API Key**: Go to API Keys section
3. **Copy your key**: Starts with `gsk_...`

## Free Tier Limits
- **14,400 requests per day**
- **30 requests per minute**
- **Fast inference** (much faster than HuggingFace)
- **Models**: Llama 3.1, Mixtral, Gemma

## Update Your Environment

Edit `backend/.env`:
```bash
# Add your Groq API key
GROQ_API_KEY=gsk_your_actual_key_here

# Keep HuggingFace for audio (ASR/TTS)
HF_API_KEY=your_huggingface_key_here
HF_API_BASE_URL=https://api-inference.huggingface.co
HF_ASR_MODEL_ID=openai/whisper-large-v3-turbo
HF_TTS_MODEL_ID=facebook/mms-tts-eng

# Enable real AI
USE_MOCK_AI=false
```

## Architecture

### Why Hybrid?
The previous setup used HuggingFace Router API which only supports LLM, not audio models. This broke mic/speaker functionality.

### New Hybrid Setup
- **LLM (Text)**: Groq API → faster, more reliable, higher token limits
- **ASR (Speech-to-Text)**: HuggingFace Inference API → free Whisper model
- **TTS (Text-to-Speech)**: HuggingFace Inference API → free MMS-TTS model

### Benefits
✅ **Mic recording works** (HF Whisper ASR)
✅ **Speaker works** (HF TTS)
✅ **Faster responses** (Groq LLM)
✅ **Better JSON parsing** (Groq has higher token limits)
✅ **100% free tier**
✅ **No more truncated responses**

## Test the Setup

```bash
cd backend
source venv/bin/activate
python test_api.py
```

Expected output:
- ✅ LLM responses from Groq
- ✅ Audio transcription from HuggingFace
- ✅ Audio synthesis from HuggingFace
- ✅ All features working

## Troubleshooting

### "GROQ_API_KEY not set"
- Make sure you added `GROQ_API_KEY=gsk_...` to `backend/.env`
- Restart the backend server

### "HF_API_KEY not set"
- Keep your HuggingFace key for audio services
- Both keys are needed for full functionality

### Still seeing mock responses
- Check `USE_MOCK_AI=false` in `.env`
- Verify both API keys are set
- Restart backend: `./dev-stop.sh && ./dev-start.sh`
