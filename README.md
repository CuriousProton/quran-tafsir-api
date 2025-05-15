# 📖 Quran Tafsir API (Arabic)

This is a FastAPI-based project that provides Quranic verse explanations (tafsir) in **Arabic** using a Large Language Model (LLM) from Groq (`llama3-70b-8192`). You provide a verse key and the corresponding Arabic text, and the API returns a detailed tafsir.

---

## 🔧 Features

- 📖 Accepts verse key (e.g., `2:3`) and verse text in Arabic
- 🤖 Uses Groq's LLM to generate simple, accurate tafsir
- 🚀 Built with FastAPI for fast and easy API development
- 📦 Includes health check endpoint
- 🔐 API key management using `.env` (do **not** commit `.env` to GitHub!)

---

## 📁 Project Structure
quran-tafsir-api/ 
  │ 
  ├── main.py # FastAPI app 
  ├── quran_arabic.csv # CSV with Quran verse keys and Arabic text 
  ├── .env # (excluded) Contains your GROQ_API_KEY 
  ├── .gitignore # Ignore venv, .env, etc. 
  └── README.md

## Install dependencies:
pip install -r requirements.txt

## Environment Variables
Create a .env file in the project root:

GROQ_API_KEY=your-groq-api-key-here
Make sure to add .env to your .gitignore to avoid pushing secrets.

## How to Use
▶️ Run the FastAPI App
uvicorn main:app --reload

🔁 Endpoints
1. POST /tafsir
Returns Arabic tafsir for a given verse.

Request body:
{
  "verse_key": "2:3",
  "verse_text": "ٱلَّذِينَ يُؤْمِنُونَ بِٱلْغَيْبِ وَيُقِيمُونَ ٱلصَّلَوٰةَ"
}
Response:
{
  "reference": "2:3",
  "text": "ٱلَّذِينَ يُؤْمِنُونَ بِٱلْغَيْبِ وَيُقِيمُونَ ٱلصَّلَوٰةَ",
  "tafsir": "تفسير الآية باللغة العربية الفصحى ..."
}

2. GET /health
Simple health check:
{
  "status": "ok",
  "quran_verses_loaded": 6236
}

