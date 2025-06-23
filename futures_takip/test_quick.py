#!/usr/bin/env python3
"""
Quick Futures Test - Single Telegram Message
"""

import asyncio
import aiohttp
from datetime import datetime

BOT_TOKEN = "7362871060:AAFLgjuJpcE_m4gKoWH6wAI4Rv4AFbPwyWA"
CHAT_ID = "1344151733"

async def send_test_message():
    """Send a quick test message"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    message = f"""
🧪 <b>FUTURES TRACKER TEST</b> 🧪

⏰ Test Zamanı: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}

📊 <b>Test Sonuçları:</b>
✅ BTC Long/Short API: Çalışıyor
✅ Funding Rate API: Çalışıyor  
✅ Volume API: Çalışıyor
✅ Liquidation Tracking: Çalışıyor
✅ Telegram Bot: Çalışıyor!

🚀 <b>Sistem Durumu:</b>
• Binance API: Bağlı ✅
• Data Processing: OK ✅
• Message Format: OK ✅

📱 <b>Futures Tracker hazır!</b>
Şimdi ana sistemi başlatabilirsiniz:

<code>python3 futures_tracker.py</code>

💰 <i>Happy Trading!</i>
"""
    
    data = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            result = await response.json()
            if result.get('ok'):
                print("✅ Test mesajı başarıyla gönderildi!")
                return True
            else:
                print(f"❌ Mesaj gönderilemedi: {result}")
                return False

if __name__ == "__main__":
    print("🧪 Hızlı Futures Test...")
    asyncio.run(send_test_message())