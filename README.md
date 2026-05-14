# 🌤 Weather Agent

A conversational AI agent that delivers real-time weather data while remembering facts about the user across sessions.

Built with the **Google Gemini API** (function calling), **OpenWeatherMap**, and a lightweight JSON-based long-term memory system.

---

## Features

| Feature | Details |
|---|---|
| **Real-time weather** | Temperature, feels-like, humidity, wind speed, and sky conditions for any city |
| **Long-term memory** | Stable facts (name, home city, preferences) are extracted from conversation and persisted in `stored_memory.json` |
| **Personalised responses** | Relevant memory is injected as context on every turn |
| **Robust error handling** | Network timeouts, bad API keys, unknown cities — all return clean error messages |
| **Rolling conversation window** | History is capped at 10 turns to stay within token limits |

---

## Project Structure

```
Weather-Agent/
├── execution.py        # CLI entry point
├── project.py          # Gemini agent with tool-use orchestration
├── factual_memory.py   # LLM-powered fact extraction & JSON persistence
├── weather.py          # OpenWeatherMap API wrapper
├── stored_memory.json  # Auto-generated persistent memory store
├── .env                # API keys (never commit this)
└── requirements.txt
```

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/SanwalSharafat/Weather-Agent.git
cd Weather-Agent
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API keys

Create a `.env` file in the project root:

```env
GEMINAI_KEY=your_google_gemini_api_key
API_KEY=your_openweathermap_api_key
```

- Get a Gemini key: <https://aistudio.google.com/app/apikey>
- Get an OpenWeatherMap key: <https://openweathermap.org/api>

### 4. Run

```bash
python execution.py
```

---

## Example Session

```
╔══════════════════════════════════════════╗
║        🌤  Weather Agent  v2.0           ║
║  Ask me about the weather anywhere!      ║
║  Type 'exit' to quit.                    ║
╚══════════════════════════════════════════╝

You: My name is Sanwal and I live in Rawalpindi
Assistant: Nice to meet you, Sanwal! I've noted that you're based in Rawalpindi.

You: What's the weather like here?
Assistant: Right now in Rawalpindi it's 32 °C (feels like 36 °C), with partly cloudy skies,
humidity at 55%, and a light breeze at 3.2 m/s.
```

---

## Requirements

```
google-genai
requests
python-dotenv
```

---

