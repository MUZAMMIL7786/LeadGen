# wakilz Voice Bot Backend

AI-powered voice agent for outbound sales calls with multilingual support (English, Hindi, Telugu).

## Overview

This backend application uses **Pipecat AI** framework to create a real-time conversational voice agent that:
- Conducts automated sales calls with natural language understanding
- Supports multiple languages with automatic routing
- Integrates with Google LLM (Gemini) for intelligent responses
- Uses Sarvam AI for speech-to-text and text-to-speech
- Includes Voice Activity Detection (VAD) for natural turn-taking

## Tech Stack

- **Pipecat AI**: Real-time voice conversation framework
- **Google Gemini**: LLM for conversation intelligence
- **Sarvam AI**: Multilingual STT/TTS services
- **WebRTC**: Real-time audio streaming
- **Silero VAD**: Voice activity detection
- **Python 3.8+**: Runtime environment

## Files

- `app.py` - Main application entry point and pipeline setup
- `prompts.py` - LLM system prompt builder for sales conversations
- `knowledge_base.py` - Product catalog and company information
- `language_router.py` - Automatic language detection and routing
- `requirements.txt` - Python dependencies
- `current_lead.json` - Simulated CRM lead data (created at runtime)

## Setup

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv

# Activate on macOS/Linux
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# Google AI (Gemini LLM)
GOOGLE_API_KEY=your_google_api_key_here

# Sarvam AI (STT/TTS)
SARVAM_API_KEY=your_sarvam_api_key_here

# Optional: Daily.co for WebRTC transport
DAILY_API_KEY=your_daily_api_key_here
```

**Get API Keys:**
- Google AI: https://ai.google.dev/
- Sarvam AI: https://www.sarvam.ai/
- Daily.co: https://www.daily.co/

### 4. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:7860`

### 5. Connect to Voice Agent

1. Open `http://localhost:7860/client` in your browser
2. Allow microphone access
3. Click "Connect"
4. The bot will greet you and start the conversation

## Features

### Multilingual Support

The voice agent automatically detects and responds in:
- **English** (en-IN)
- **Hindi** (hi-IN)
- **Telugu** (te-IN)

Language routing is handled by `LanguageRouterProcessor` which analyzes incoming speech and switches the TTS voice accordingly.

### Sales Conversation Flow

1. **Greeting** - Agent introduces itself as wakilz sales representative
2. **Discovery** - Asks about lead's business needs
3. **Product Pitch** - Presents relevant AI solutions
4. **Objection Handling** - Addresses concerns naturally
5. **Call-to-Action** - Books a demo or schedules follow-up

### Knowledge Base

The agent has access to:
- AI Lead Qualification solutions
- Sales Automation products
- Voice Bot services
- Integration capabilities (HubSpot, Salesforce, etc.)
- Pricing and ROI metrics

## Customization

### Modify Sales Prompts

Edit `prompts.py` to change the agent's personality, conversation flow, or sales strategy:

```python
def build_system_prompt(lead_data: dict):
    # Customize the prompt here
    return f"You are {lead_data['agent_name']}, ..."
```

### Update Product Catalog

Edit `knowledge_base.py` to add/modify products:

```python
PRODUCTS = {
    "lead_qualification": {
        "name": "AI Lead Qualification",
        # ...
    }
}
```

### Adjust Voice Settings

In `app.py`, modify the TTS/STT services:

```python
tts = SarvamTTSService(
    api_key=os.getenv("SARVAM_API_KEY"),
    voice="arvind",  # Change voice here
    language=Language.EN_IN
)
```

## Troubleshooting

### "Module not found" errors
```bash
pip install --upgrade -r requirements.txt
```

### Microphone not working
- Check browser permissions (Chrome/Firefox)
- Ensure WebRTC is supported
- Try accessing via `https://` instead of `http://`

### API rate limits
- Check your API key quotas
- Add retry logic in `app.py` if needed

### Voice latency
- Reduce VAD `stop_secs` parameter in `app.py`
- Use faster LLM models (e.g., Gemini Flash)
- Optimize network connection

## Development

### Testing CRM Integration

Before connecting, run the trigger script to simulate a CRM lead:

```bash
python trigger_call.py
```

This creates `current_lead.json` with sample lead data.

### Adding New Languages

1. Add language constant in `pipecat.transcriptions.language`
2. Update `language_router.py` to handle new language
3. Configure Sarvam AI with appropriate voice

### Logging

Logs are handled by `loguru`. Adjust verbosity in `app.py`:

```python
logger.add("voice_bot.log", level="DEBUG")
```

## Production Deployment

### Environment

- Use production `.env` with real API keys
- Set up SSL/TLS for HTTPS
- Deploy on cloud platform (AWS, GCP, Azure)
- Use managed Daily.co rooms for WebRTC

### Scaling

- Run multiple instances behind load balancer
- Use Redis for session management
- Implement proper error handling and retries
- Monitor API usage and costs

### Security

- Never commit `.env` files
- Rotate API keys regularly
- Implement rate limiting
- Validate all user inputs

## Integration with Frontend

The voice bot backend is designed to work with `voicebot.html` in the parent directory. The frontend connects via WebRTC and provides the user interface for the voice conversation.

### How It Works

1. **Start the Backend**: Run `python app.py` to start the Pipecat voice agent on `localhost:7860`
2. **Open the Frontend**: Navigate to the parent directory and open `voicebot.html` in your browser
3. **Start a Call**: Click "Click to Start Call" button
4. **Natural Conversation**:
   - The agent uses Silero VAD (Voice Activity Detection) to detect when you're speaking
   - Speak naturally - the agent will respond automatically after you finish talking
   - You can interrupt the agent at any time by speaking
   - The conversation transcript appears in real-time on the right side

### Architecture

- **Transport**: WebRTC for real-time bidirectional audio streaming
- **Signaling**: WebSocket connection for SDP offer/answer exchange and ICE candidate trickle
- **Audio Processing**:
  - Microphone input → WebRTC → Pipecat → Sarvam STT → Google Gemini LLM
  - Google Gemini LLM → Sarvam TTS → Pipecat → WebRTC → Browser audio output
- **Turn-Taking**: Silero VAD on backend handles natural conversation flow

### Accessing the Demo

**Local Development:**
```bash
# Terminal 1 - Start backend
cd backend
source .venv/bin/activate
python app.py

# Terminal 2 - Serve frontend (optional, can also open file directly)
cd ..
npx serve .
# Open http://localhost:3000/voicebot.html
```

**Direct File Access:**
- Simply open `voicebot.html` in Chrome/Firefox after starting the backend
- Click "Click to Start Call" and allow microphone access

### Troubleshooting

**Connection Issues:**
- Ensure backend is running on port 7860
- Check browser console for WebRTC errors
- Verify microphone permissions are granted
- Try accessing via `http://` not `https://` for local testing

**Audio Issues:**
- Ensure microphone is not being used by another application
- Check browser audio output settings
- Verify Sarvam AI API key is valid in backend `.env`

**Backend Not Starting:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check `.env` file has required API keys (GOOGLE_API_KEY, SARVAM_API_KEY)
- Check logs for specific error messages

## License

See root repository LICENSE file.

## Support

For issues or questions:
- Check Pipecat AI docs: https://docs.pipecat.ai/
- Email: support@wakilz.com
