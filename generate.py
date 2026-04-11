import streamlit as st
import asyncio
import time
from openai import AsyncOpenAI
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Ortam değişkenlerini ve temayı yükle (secrets.toml ve config.toml)
st.set_page_config(layout="wide")
st.title("🌌 Multi-LLM Arena: Speed & Quality Battle")

# --- Model Bağlantılarını Hazırla ---

# 1. OpenAI
client_openai = AsyncOpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 2. DeepSeek (OpenAI API uyumlu)
client_deepseek = AsyncOpenAI(
    api_key=st.secrets["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com/v1"  # Kritik nokta!
)

# 3. Gemini
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model_gemini = genai.GenerativeModel('gemini-1.5-flash-latest')


# --- Asenkron LLM Çağrı Fonksiyonları ---

async def ask_openai(prompt, st_col):
    start = time.time()
    try:
        response = await client_openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        latency = time.time() - start
        st_col.write(f"**OpenAI Cevabı:**\n\n{response.choices[0].message.content}")
        st_col.metric("Süre (sn)", f"{latency:.2f}s")
    except Exception as e:
        st_col.error(f"Error: {e}")


async def ask_deepseek(prompt, st_col):
    # Benzer yapı, DeepSeek API URL'ini kullanacak
    pass


async def ask_gemini(prompt, st_col):
    # Gemini'nin kendi asenkron metodunu kullanacağız
    pass


# --- Arayüz Kontrolü ---

user_prompt = st.text_input("Model Arena'ya bir soru sor:")

if st.button("Savaşı Başlat") and user_prompt:
    # 3 Kolon oluştur
    col1, col2, col3 = st.columns(3)

    col1.subheader("🧠 OpenAI (GPT-4o)")
    col2.subheader("⚡ DeepSeek")
    col3.subheader("🤖 Gemini")


    # Paralel çağrıları başlat
    async def run_arena():
        await asyncio.gather(
            ask_openai(user_prompt, col1),
            ask_deepseek(user_prompt, col2),
            ask_gemini(user_prompt, col3)
        )


    # Asenkron akışı çalıştır
    asyncio.run(run_arena())