import asyncio
from anthropic import AsyncAnthropic

async def test():
    client = AsyncAnthropic()
    try:
        message = await client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=10,
            messages=[{"role": "user", "content": "Merhaba"}]
        )
        print("Bağlantı Başarılı:", message.content[0].text)
    except Exception as e:
        print("Hata devam ediyor:", e)

asyncio.run(test())