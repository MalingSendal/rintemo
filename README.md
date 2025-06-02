# RinAI &nbsp; <img src="https://web.whatsapp.com/img/bg-chat-tile-light_a4be512e7195b6b733d9110b408f075d.png" height="32" align="right">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20API-lightgrey?logo=flask)
![Discord](https://img.shields.io/badge/Discord-Bot-5865F2?logo=discord)
![NLP](https://img.shields.io/badge/NLP-SentenceTransformers-green?logo=ai)
![License](https://img.shields.io/badge/License-Private-red)

---

<img src="appearance/ChatGPT%20Image%20May%2031,%202025,%2010_44_50%20AM.png" width="200" align="right" style="border-radius: 12px; margin-left: 20px;">

## 🌸 RinAI: Your Evolving AI Companion

**RinAI** is a personality-rich, memory-augmented AI chatbot and Discord bot. RinAI remembers your facts, evolves her personality, and adapts her quirks and traits based on your interactions. She can chat via a web interface or Discord, and even generate voice responses!

---

## ✨ Features

- **🧠 Long-Term Memory:** Remembers user facts, preferences, and conversation history.
- **🎭 Dynamic Personality:** Evolves traits and quirks based on user interactions and facts.
- **💬 Web Chat UI:** WhatsApp-inspired chat interface with timestamps and voice playback.
- **🤖 Discord Bot:** Chat with RinAI directly in your Discord server.
- **🗣️ Voice Synthesis:** Generates voice responses using TTS (gTTS).
- **⏰ Time Awareness:** Recognizes time since last interaction and adapts responses accordingly.
- **📚 Fact Extraction:** Learns and stores facts about users from conversations.
- **🔗 Embedding Memory:** Uses sentence-transformers for semantic memory and context.
- **📝 Persistent Storage:** Stores memory, facts, and personality in JSON/CSV files.
- **🌈 Customizable Personality:** Easily tweakable via `personality.json` and user facts.

---

## 🗂️ Project Structure

```
.
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── config.py            # Config and system prompt
│   ├── facts.py             # Fact extraction and memory
│   ├── llm_client.py        # LLM API integration
│   ├── memory.py            # Long-term memory logic
│   ├── personality.py       # Personality evolution logic
│   ├── routes.py            # Flask routes
├── templates/
│   └── index.html           # Web chat UI
├── appearance/
│   └── ...                  # Images and avatars
├── songs/
│   └── ...                  # Songs
├── discord_bot.py           # Discord bot integration
├── main.py                  # App entrypoint
├── requirements.txt         # Python dependencies
├── personality.json         # Persistent personality state
├── user_facts.json          # User facts and rules
├── interaction_memory.json  # Last interaction timestamps
├── chat_memory.csv          # Conversation logs
├── facts_memory.csv         # Extracted user facts
├── response.mp3             # Voice response output
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```sh
git clone https://github.com/MalingSendal/rintemo.git
cd rintemo
```

### 2. Install Dependencies

```sh
pip install -r requirements.txt
```

### 3. Set Up Environment

Create a `.env` file with your Discord token and DeepSeek API:

```
DEEPSEEK_API_KEY=your_API_here
DISCORD_TOKEN=your_discord_token_here
```

### 4. Run the Web App

```sh
python3 main.py
```

Visit [http://localhost:5000](http://localhost:5000) to chat with RinAI.

### 5. Run the Discord Bot

```sh
python discord_bot.py
```

---

## 🖼️ Rin Profile Picture

![Rin Appearance](appearance/Rin.png)

---

## 🤖 Discord Integration

- Use `!rin` as a prefix to chat with RinAI in Discord.
- RinAI will remember facts and evolve her personality per user.

---

## 🧩 Personality & Memory

- **Personality:** Defined and evolved in [`app/personality.py`](app/personality.py) and [`personality.json`](personality.json).
- **Facts:** Extracted and stored in [`user_facts.json`](user_facts.json) and [`facts_memory.csv`](facts_memory.csv).
- **Memory:** Embeddings and texts stored in [`personality.json`](personality.json) and [`interaction_memory.json`](interaction_memory.json).

---

## 🛠️ Technologies Used

- **Python 3.10+**
- **Flask** (Web API)
- **Discord.py** (Discord bot)
- **sentence-transformers** (Semantic embeddings)
- **pyttsx3** (Text-to-speech)
- **scikit-learn** (NLP utilities)
- **dotenv** (Environment variables)

---

## 📄 License

This project is **private** and not licensed for public/commercial use.

---

## 💡 Credits

- Created by Rendy and contributors.
- Inspired by conversational AI and memory-augmented agents.

---

> _"I'm Rin, your evolving AI companion. Let's grow together—one chat at a time!"_
