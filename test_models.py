import asyncio
from anthropic import AsyncAnthropic

async def test():
    client = AsyncAnthropic(api_key="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")
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