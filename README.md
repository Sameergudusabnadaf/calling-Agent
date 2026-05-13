# Custom AI Voice Agent — Lily (Flora Flower Shop)

This project implements a fully custom AI voice agent that can answer customer phone calls, handle business queries, and log conversations to Airtable.

## Architecture

`Customer Call -> Twilio -> LiveKit SIP -> Deepgram (STT) -> OpenAI (LLM) -> ElevenLabs (TTS) -> Customer`

## Features

- **Real-time Voice Streaming**: Low latency interaction using LiveKit.
- **Natural AI Responses**: Powered by OpenAI's GPT-4o.
- **Human-like Speech**: Using ElevenLabs for high-quality TTS.
- **Fast Transcription**: Deepgram provides real-time STT.
- **CRM Integration**: All calls are logged to Airtable.

## Setup Instructions

### 1. Prerequisites

- Python 3.11+
- [LiveKit Cloud](https://livekit.io/) or self-hosted instance.
- [Deepgram API Key](https://deepgram.com/)
- [OpenAI API Key](https://platform.openai.com/)
- [ElevenLabs API Key](https://elevenlabs.io/)
- [Airtable Personal Access Token](https://airtable.com/)
- [Twilio Account](https://twilio.com/)

### 2. Installation

1. Clone the repository and navigate to the directory.
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your API keys:
   ```bash
   cp .env.example .env
   ```

### 3. Twilio & LiveKit SIP Setup

1. **Twilio**: Buy a voice-enabled phone number.
2. **LiveKit SIP**:
   - Go to your LiveKit Cloud dashboard.
   - Navigate to **SIP** and create a new **SIP Trunk**.
   - Copy the SIP URI provided by LiveKit.
3. **Twilio Routing**:
   - The easiest way to route calls is using a **TwiML Bin**.
   - Create a new TwiML Bin in Twilio with the following XML (replace `your-sip-uri` with the one from LiveKit):
     ```xml
     <?xml version="1.0" encoding="UTF-8"?>
     <Response>
         <Dial>
             <Sip>sip:your-sip-uri@sip.livekit.cloud</Sip>
         </Dial>
     </Response>
     ```
   - Go to your Twilio Phone Number settings, and under **Voice & Fax**, set "A Call Comes In" to **TwiML Bin** and select the one you just created.

### 4. Airtable Setup

Create a base in Airtable with a table named `CallLogs` (or as configured in `.env`) with the following columns:

- `Caller Number` (Single line text)
- `Duration` (Single line text)
- `Transcript` (Long text)
- `Timestamp` (Single line text or Date)

### 5. Running the Agent

Start the agent worker:

```bash
python agent.py dev
```

## Troubleshooting

- **No Voice**: Check your ElevenLabs API key and ensure the `ELEVENLABS_VOICE_ID` is valid.
- **Transcription Failures**: Ensure Deepgram credits are available.
- **Airtable Errors**: Verify your Token and Base ID.
  **Developed by: SAMEER NADAF**
