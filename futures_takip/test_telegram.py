#!/usr/bin/env python3
"""
Test Telegram send function specifically
"""

import asyncio
import aiohttp

BOT_TOKEN = "7362871060:AAFLgjuJpcE_m4gKoWH6wAI4Rv4AFbPwyWA"
CHAT_ID = "1344151733"

async def test_send():
    """Test Telegram message sending"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    # Test message similar to futures report
    message = """
📊 <b>FUTURES REPORT</b> 📊
⏰ 09:25 UTC

🟡 NEUTRAL Market Sentiment

━━━ <b>₿ BTC</b> ━━━
💰 $101,768 (-1.0%)
📊 Vol: $27.93B
📈 L/S: <b>1.17</b> (54%L)
💸 Fund: <b>-0.002%</b>
⚡ Liq: 0 işlem

━━━ <b>🔥 SOL</b> ━━━
💰 $133.9 (-1.6%)
📊 Vol: $4.18B
📈 L/S: <b>2.73</b> (73%L)
💸 Fund: <b>-0.005%</b>
⚡ Liq: 0 işlem

💡 <b>Key Levels:</b>
L/S>2.0=Bearish | L/S<0.5=Bullish
Fund>0.1%=Bearish | Fund<-0.05%=Bullish
"""
    
    data = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    
    print("📱 Telegram'a gönderiliyor...")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data) as response:
                result = await response.json()
                print(f"Response: {result}")
                if result.get('ok'):
                    print("✅ Mesaj başarıyla gönderildi!")
                    return True
                else:
                    print(f"❌ Hata: {result.get('description', 'Bilinmeyen hata')}")
                    return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_send())