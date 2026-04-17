import streamlit as st
import asyncio
import time
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
import google.generativeai as genai
from anthropic import AsyncAnthropic

# 1. Ortam Değişkenlerini Yükle
load_dotenv()

# 2. Sayfa Yapılandırması
st.set_page_config(page_title="LLM 3 Clash (Normal)", layout="wide")
st.title("🌌 LLM 3 Clash")

# --- SIDEBAR: Model Seçimleri ---
with st.sidebar:
    st.header("⚙️ Model Seçimleri")
    oa_model = st.selectbox("OpenAI Modeli", ["gpt-4o-mini", "gpt-4o"], index=0)
    ds_model = st.selectbox("DeepSeek Modeli", ["deepseek-chat", "deepseek-coder"], index=0)
    ge_model = st.sidebar.selectbox(
        "Gemini Modeli",
        ["models/gemini-2.5-pro-preview-tts"],
        index=0
    )
    ca_model = st.selectbox("Claude Modeli", ["claude-3-5-sonnet-20240620"], index=0)



# --- API İstemcileri ---
client_openai = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client_claude = AsyncAnthropic(api_key=os.getenv("CLAUDE_API_KEY"))
client_deepseek = AsyncOpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com/v1")



import google.generativeai as genai
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY"),
    transport='rest'
)




async def ask_openai(prompt, container, model_name):
    start_time = time.time()
    try:
        response = await client_openai.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "Sen yardımcı bir asistansın. Türkçe cevap ver."},
                {"role": "user", "content": prompt}
            ],
            stream=False  # Streaming kapalı
        )
        duration = time.time() - start_time
        answer = response.choices[0].message.content
        container.markdown(answer)
        return duration
    except Exception as e:
        container.error(f"OpenAI Hatası: {e}")
        return None



import time
import asyncio



# İstemciyi fonksiyon dışında tanımladığını varsayıyorum
# client_claude = AsyncAnthropic(api_key="API_KEY")

async def ask_claude(prompt, container, model_name="claude-3-5-sonnet-20240620"):
    start_time = time.time()
    try:
        response = await client_claude.messages.create(
            model=model_name,
            max_tokens=1024,
            system="Sen yardımcı bir asistansın. Türkçe cevap ver.",  # Sistem mesajı parametresi
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        duration = time.time() - start_time
        answer = response.content[0].text

        # Yanıtı anında ilgili Streamlit sütununa basar
        container.markdown(answer)

        return duration

    except Exception as e:
        container.error(f"Claude Hatası: {e}")
        return None



async def ask_deepseek(prompt, container, model_name):
    start_time = time.time()
    try:
        response = await client_deepseek.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "Sen yardımcı bir asistansın. Türkçe cevap ver."},
                {"role": "user", "content": prompt}
            ],
            stream=False
        )
        duration = time.time() - start_time
        answer = response.choices[0].message.content
        container.markdown(answer)
        return duration
    except Exception as e:
        container.error(f"DeepSeek Hatası: {e}")
        return None


import httpx  # Eğer yüklü değilse terminale: pip install httpx


async def ask_gemini(prompt, container, model_name):
    start_time = time.time()
    api_key = os.getenv("GEMINI_API_KEY")

    # v1beta yerine v1 kullanarak doğrudan URL oluşturuyoruz
    # Modeli 'gemini-1.5-flash' olarak sadeleştiriyoruz
    clean_model_name = model_name.replace("models/", "").replace("-latest", "")
    url = f"https://generativelanguage.googleapis.com/v1/models/{clean_model_name}:generateContent?key={api_key}"

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=30.0)
            result = response.json()

            if response.status_code == 200:
                answer = result['candidates'][0]['content']['parts'][0]['text']
                duration = time.time() - start_time
                container.markdown(answer)
                return duration
            else:
                container.error(
                    f"Gemini API Hatası ({response.status_code}): {result.get('error', {}).get('message', 'Bilinmeyen hata')}")
                return None
    except Exception as e:
        container.error(f"Bağlantı Hatası: {e}")
        return None

# --- Arayüz Kontrolü ---
prompt = st.text_area("Sorunu yaz:", placeholder="Yarışmayı başlatmak için bir şeyler yaz...")

if st.button("Savaşı Başlat 🚀"):
    if not prompt:
        st.warning("Bir soru girmelisin!")
    else:
        col1, col2, col3 = st.columns(3)

        # Metrikler ve İçerik Alanları
        m1, m2, m3 = col1.empty(), col2.empty(), col3.empty()
        c1 = col1.container(height=400)
        c2 = col2.container(height=400)
        c3 = col3.container(height=400)

        c1.info("Bekleniyor...")
        c2.info("Bekleniyor...")
        c3.info("Bekleniyor...")


        async def run_battle():
            results = await asyncio.gather(
                ask_openai(prompt, c1, oa_model),
                ask_deepseek(prompt, c2, ds_model),
                ask_claude(prompt, c3, ca_model)
            )

            # Sonuçlar geldiğinde kutuları temizle ve süreyi yaz
            if results[0]: m1.metric(f"⏱️ {oa_model}", f"{results[0]:.2f}s")
            if results[1]: m2.metric(f"⏱️ {ds_model}", f"{results[1]:.2f}s")
            if results[2]: m3.metric(f"⏱️ {ca_model}", f"{results[2]:.2f}s")


        asyncio.run(run_battle())