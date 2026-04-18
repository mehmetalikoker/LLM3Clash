
import os
from dotenv import load_dotenv
from anthropic import AsyncAnthropic
import asyncio


load_dotenv()
client_claude = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

print("--- Erişimine Açık Modeller ---")
async def list_models():
    try:
        # await şimdi çalışacaktır
        models = await client_claude.models.list()

        async for model in models:
            print(f"Model ID: {model.id}")
    except Exception as e:
        print(f"Hata: {e}")


# 2. Bu fonksiyonu asyncio ile çalıştır
if __name__ == "__main__":
    asyncio.run(list_models())

