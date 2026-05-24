# LLM Chatbot

A multi-provider LLM chatbot web app built with Streamlit — supports Groq (free), Google Gemini, and OpenAI with streaming responses, model selection, and API key management.

---

## Features

| Feature | Description |
| --- | --- |
| **Multi-Provider** | Switch between Groq (free), Google Gemini, and OpenAI from the sidebar |
| **Streaming Responses** | Real-time token-by-token output via streaming API |
| **Model Selection** | Choose from multiple models per provider (Llama, Gemma, Gemini 2.5, GPT-4o, etc.) |
| **API Key Management** | Password-masked input with direct links to get each key |
| **Advanced Parameters** | Temperature and Max tokens controls hidden in collapsible panel |
| **Chat History** | Persistent session history with one-click clear |
| **Light Theme** | Forced light theme regardless of OS/browser preference |

---

## Supported Providers & Models

| Provider | Cost | Models | Get API Key |
| --- | --- | --- | --- |
| **Groq** | Free (rate-limited) | llama-3.3-70b-versatile, llama-3.1-8b-instant, gemma2-9b-it, mixtral-8x7b-32768 | [console.groq.com/keys](https://console.groq.com/keys) |
| **Google Gemini** | Free tier available | gemini-2.5-flash, gemini-2.5-pro, gemini-3.5-flash | [aistudio.google.com/apikey](https://aistudio.google.com/apikey) |
| **OpenAI** | Paid | gpt-4o-mini, gpt-4o, gpt-4.1-mini, gpt-4.1 | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) |

---

## Tech Stack

- **Frontend:** Streamlit (wide layout, sidebar, streaming chat)
- **LLM Providers:** Groq SDK, Google GenerativeAI SDK, OpenAI SDK
- **Streaming:** Generator functions + `st.write_stream()`
- **Styling:** Custom CSS, forced light theme via `.streamlit/config.toml`

---

## Getting Started

### Installation

```bash
git clone https://github.com/khala1391/llm_chatbot.git
cd llm_chatbot
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### Run

```bash
streamlit run chatbot.py
```

Open `http://localhost:8501`

---

## Usage

1. **Select provider** — choose Groq (free), Google Gemini, or OpenAI from the sidebar radio buttons
2. **Enter API key** — paste your key into the password field (links to get each key are provided)
3. **Select model** — pick from the dropdown list for your chosen provider
4. **Adjust parameters** *(optional)* — expand ⚙️ Advanced to set Temperature and Max tokens
5. **Start chatting** — type in the chat input and get streaming responses
6. **Clear history** — click 🗑️ Clear Chat to start a new conversation

---

## Project Structure

```text
llm_chatbot/
├── chatbot.py              # Main Streamlit app
├── requirements.txt        # Python dependencies
├── .streamlit/
│   └── config.toml         # Theme configuration (force light mode)
└── assets/
    └── Yuttapong M.jpg     # Profile image
```

---

## Author

Yuttapong M. — [linkedin.com/in/yuttapong-m](https://www.linkedin.com/in/yuttapong-m/)
