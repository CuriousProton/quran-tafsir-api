from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from groq import Groq
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Load Groq API key
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise EnvironmentError("GROQ_API_KEY environment variable not set.")

client = Groq(api_key=api_key)

# Load Quran data
try:
    data = pd.read_csv('quran_arabic.csv', encoding='utf-8')
    new_data = data[['verse_key', 'text_uthmani']]
    verse_dict = dict(zip(new_data['verse_key'], new_data['text_uthmani']))
except FileNotFoundError:
    raise FileNotFoundError("CSV file 'quran_arabic.csv' not found. Please check the path.")

# Request schema
class TafsirRequest(BaseModel):
    verse_key: str  # e.g., "1:2"
    verse_text: str  # e.g., "ٱلْحَمْدُ لِلَّهِ رَبِّ ٱلْعَـٰلَمِينَ"

# Build LLM prompt
def build_arabic_prompt(reference: str, text: str) -> str:
    return (
        "أنت عالم متخصص في تفسير القرآن الكريم.\n"
        "يرجى تقديم تفسير شامل ومبسط للآية التالية، مع الأخذ بعين الاعتبار رقم السورة ورقم الآية:\n\n"
        f"{reference}\t{text}\n\n"
        "اكتب التفسير باللغة العربية الفصحى وبأسلوب واضح وميسر للقارئ العام."
    )

# Call Groq LLM
def query_llm_arabic(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content  
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM Error: {str(e)}")

# Full tafsir workflow
def get_tafsir_from_input(verse_key: str, verse_text: str) -> dict:
    prompt = build_arabic_prompt(verse_key, verse_text)
    tafsir = query_llm_arabic(prompt)
    return {"reference": verse_key, "text": verse_text, "tafsir": tafsir}

# Route: Tafsir
@app.post("/tafsir")
async def get_tafsir(request: TafsirRequest):
    return get_tafsir_from_input(request.verse_key, request.verse_text)

# Health check
@app.get("/health")
def health_check():
    return {"status": "ok", "quran_verses_loaded": len(verse_dict)}