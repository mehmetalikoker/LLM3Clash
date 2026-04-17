import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("ANTHROPIC_API_KEY"))

print("--- Erişimine Açık Modeller ---")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Model Adı: {m.name}")
except Exception as e:
    print(f"Hata oluştu: {e}")



import anthropic

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

message = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=100,
    messages=[{"role": "user", "content": "Merhaba!"}]
)
print(message.content)


