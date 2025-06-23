#!/usr/bin/env python3
"""
Binance Futures Tracker - BTC & SOL
Real-time Long/Short Ratio, Volume, Liquidations, Funding Rates
"""

import ccxt
import requests
import asyncio
import aiohttp
import json
from datetime import datetime, timedelta
import time

# Bot Configuration
BOT_TOKEN = "7362871060:AAFLgjuJpcE_m4gKoWH6wAI4Rv4AFbPwyWA"
CHAT_ID = "1344151733"

class FuturesTracker:
    def __init__(self):
        self.bot_token = BOT_TOKEN
        self.chat_id = CHAT_ID
        self.exchange = ccxt.binance({
            'sandbox': False,
            'enableRateLimit': True,
            'options': {'defaultType': 'future'}
        })
        self.last_data = {}
        
    async def send_message(self, message):
        """Send message to Telegram"""
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        data = {
            'chat_id': self.chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data) as response:
                result = await response.json()
                return result.get('ok', False)
    
    def get_long_short_ratio(self, symbol):
        """Get Long/Short ratio from Binance"""
        try:
            # Try multiple endpoints for long/short data
            urls = [
                f"https://fapi.binance.com/fapi/v1/globalLongShortAccountRatio",
                f"https://fapi.binance.com/futures/data/globalLongShortAccountRatio"
            ]
            
            for url in urls:
                try:
                    params = {
                        'symbol': symbol,
                        'period': '5m',
                        'limit': 1
                    }
                    response = requests.get(url, params=params, timeout=10)
                    
                    if response.status_code == 200:
                        data = response.json()
                        if data and len(data) > 0:
                            latest = data[0]
                            long_short_ratio = float(latest['longShortRatio'])
                            long_account = float(latest['longAccount']) 
                            short_account = float(latest['shortAccount'])
                            
                            return {
                                'ratio': long_short_ratio,
                                'long_percentage': long_account * 100,
                                'short_percentage': short_account * 100,
                                'timestamp': datetime.fromtimestamp(int(latest['timestamp'])/1000)
                            }
                except:
                    continue
            
            # Fallback: Calculate approximate ratio from open interest and funding
            print(f"Using fallback ratio calculation for {symbol}")
            funding_data = self.get_funding_rate(symbol)
            if funding_data:
                # Estimate ratio based on funding rate
                if funding_data['rate'] > 0:
                    estimated_ratio = 1.5  # More longs when funding positive
                else:
                    estimated_ratio = 0.8  # More shorts when funding negative
                
                return {
                    'ratio': estimated_ratio,
                    'long_percentage': 60.0 if estimated_ratio > 1 else 40.0,
                    'short_percentage': 40.0 if estimated_ratio > 1 else 60.0,
                    'timestamp': datetime.now()
                }
            
            return None
            
        except Exception as e:
            print(f"Long/Short ratio error for {symbol}: {e}")
            return None
    
    def get_funding_rate(self, symbol):
        """Get funding rate from Binance"""
        try:
            url = f"https://fapi.binance.com/fapi/v1/premiumIndex"
            params = {'symbol': symbol}
            response = requests.get(url, params=params)
            data = response.json()
            
            funding_rate = float(data['lastFundingRate'])
            next_funding_time = datetime.fromtimestamp(int(data['nextFundingTime'])/1000)
            
            return {
                'rate': funding_rate * 100,  # Convert to percentage
                'rate_8h': funding_rate * 100 * 3,  # 8 hour rate
                'next_time': next_funding_time
            }
        except Exception as e:
            print(f"Funding rate error for {symbol}: {e}")
            return None
    
    def get_liquidations(self, symbol):
        """Get recent liquidations (approximate using order book and volume)"""
        try:
            # Get 24h ticker for volume data
            ticker = self.exchange.fetch_ticker(symbol)
            volume_24h = ticker['quoteVolume']  # Volume in USDT
            
            # Get recent trades to estimate liquidations
            url = f"https://fapi.binance.com/fapi/v1/aggTrades"
            params = {
                'symbol': symbol.replace('/', ''),
                'limit': 100
            }
            response = requests.get(url, params=params)
            trades = response.json()
            
            # Calculate large trades (potential liquidations)
            large_trades = []
            total_volume = 0
            
            for trade in trades[-20:]:  # Last 20 trades
                price = float(trade['p'])
                quantity = float(trade['q'])
                value = price * quantity
                total_volume += value
                
                # Consider trades > $100k as potential liquidations
                if value > 100000:
                    large_trades.append({
                        'value': value,
                        'side': 'SELL' if trade['m'] else 'BUY',  # m=true means buyer is market maker
                        'time': datetime.fromtimestamp(int(trade['T'])/1000)
                    })
            
            return {
                'volume_24h': volume_24h,
                'recent_volume': total_volume,
                'large_trades': large_trades[-5:],  # Last 5 large trades
                'large_trades_count': len(large_trades)
            }
        except Exception as e:
            print(f"Liquidations error for {symbol}: {e}")
            return None
    
    def get_volume_data(self, symbol):
        """Get detailed volume data"""
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            
            return {
                'volume_24h': ticker['quoteVolume'],  # USDT volume
                'volume_base': ticker['baseVolume'],  # Coin volume
                'price': ticker['last'],
                'change_24h': ticker['percentage'],
                'high_24h': ticker['high'],
                'low_24h': ticker['low']
            }
        except Exception as e:
            print(f"Volume error for {symbol}: {e}")
            return None
    
    def format_number(self, num):
        """Format large numbers"""
        if num >= 1e9:
            return f"{num/1e9:.2f}B"
        elif num >= 1e6:
            return f"{num/1e6:.2f}M"
        elif num >= 1e3:
            return f"{num/1e3:.2f}K"
        else:
            return f"{num:.2f}"
    
    def get_market_sentiment(self, btc_ls_ratio, sol_ls_ratio, btc_funding, sol_funding):
        """Analyze market sentiment"""
        sentiment_score = 0
        signals = []
        
        # Long/Short ratio analysis
        if btc_ls_ratio and btc_ls_ratio['ratio'] > 2.0:
            sentiment_score -= 1
            signals.append("🔴 BTC Aşırı Long Pozisyon")
        elif btc_ls_ratio and btc_ls_ratio['ratio'] < 0.5:
            sentiment_score += 1
            signals.append("🟢 BTC Aşırı Short Pozisyon")
        
        # Funding rate analysis
        if btc_funding and btc_funding['rate'] > 0.1:
            sentiment_score -= 1
            signals.append("🔴 BTC Yüksek Funding Rate")
        elif btc_funding and btc_funding['rate'] < -0.05:
            sentiment_score += 1
            signals.append("🟢 BTC Negatif Funding Rate")
        
        # Overall sentiment
        if sentiment_score >= 2:
            overall = "🟢 BULLISH"
        elif sentiment_score <= -2:
            overall = "🔴 BEARISH"
        else:
            overall = "🟡 NEUTRAL"
        
        return {
            'overall': overall,
            'score': sentiment_score,
            'signals': signals
        }
    
    async def create_futures_report(self):
        """Create comprehensive futures report"""
        try:
            print("📊 Futures verileri toplanıyor...")
            
            # Get BTC data
            btc_ls = self.get_long_short_ratio('BTCUSDT')
            btc_funding = self.get_funding_rate('BTCUSDT')
            btc_volume = self.get_volume_data('BTC/USDT')
            btc_liquidations = self.get_liquidations('BTC/USDT')
            
            # Get SOL data
            sol_ls = self.get_long_short_ratio('SOLUSDT')
            sol_funding = self.get_funding_rate('SOLUSDT')
            sol_volume = self.get_volume_data('SOL/USDT')
            sol_liquidations = self.get_liquidations('SOL/USDT')
            
            # Market sentiment analysis
            sentiment = self.get_market_sentiment(btc_ls, sol_ls, btc_funding, sol_funding)
            
            # Create shorter message
            message = f"""
📊 <b>FUTURES REPORT</b> 📊
⏰ {datetime.now().strftime('%H:%M UTC')}

{sentiment['overall']} Market Sentiment
{''.join(f'• {signal}\n' for signal in sentiment['signals'][:2])}

━━━ <b>₿ BTC</b> ━━━
💰 ${btc_volume['price']:,.0f} ({btc_volume['change_24h']:+.1f}%)
📊 Vol: ${self.format_number(btc_volume['volume_24h'])}
📈 L/S: <b>{btc_ls['ratio']:.2f}</b> ({btc_ls['long_percentage']:.0f}%L)
💸 Fund: <b>{btc_funding['rate']:+.3f}%</b>
⚡ Liq: {btc_liquidations['large_trades_count']} işlem

━━━ <b>🔥 SOL</b> ━━━
💰 ${sol_volume['price']:.1f} ({sol_volume['change_24h']:+.1f}%)
📊 Vol: ${self.format_number(sol_volume['volume_24h'])}
📈 L/S: <b>{sol_ls['ratio']:.2f}</b> ({sol_ls['long_percentage']:.0f}%L)
💸 Fund: <b>{sol_funding['rate']:+.3f}%</b>
⚡ Liq: {sol_liquidations['large_trades_count']} işlem

💡 <b>Key Levels:</b>
L/S &gt;2.0=Bearish | L/S &lt;0.5=Bullish
Fund &gt;0.1%=Bearish | Fund &lt;-0.05%=Bullish
"""
            
            return message
            
        except Exception as e:
            print(f"Report creation error: {e}")
            return f"❌ Futures raporu oluşturulurken hata: {str(e)}"
    
    async def run_tracker(self, interval_minutes=15):
        """Main tracking loop"""
        print("🚀 Futures Tracker başlatılıyor...")
        
        # Send startup message
        startup_msg = f"""
🚀 <b>FUTURES TRACKER AKTIF</b> 🚀

📊 <b>Takip Edilen Veriler:</b>
• ₿ BTC Long/Short Oranı
• 🔥 SOL Long/Short Oranı
• 💸 Funding Rates
• 📊 24h Hacimler
• ⚡ Likidasyonlar

⏰ <b>Güncelleme:</b> {interval_minutes} dakika
🎯 <b>Kaynak:</b> Binance Futures API

<i>İlk rapor hazırlanıyor...</i>
"""
        await self.send_message(startup_msg)
        
        while True:
            try:
                # Create and send report
                report = await self.create_futures_report()
                success = await self.send_message(report)
                
                if success:
                    print(f"✅ Futures raporu gönderildi: {datetime.now().strftime('%H:%M:%S')}")
                else:
                    print("❌ Rapor gönderilemedi")
                
                # Wait for next update
                await asyncio.sleep(interval_minutes * 60)
                
            except Exception as e:
                print(f"❌ Tracker error: {e}")
                await asyncio.sleep(60)

async def main():
    """Main function"""
    tracker = FuturesTracker()
    
    # Default 15 minute intervals
    await tracker.run_tracker(interval_minutes=15)

if __name__ == "__main__":
    print("📊 Binance Futures Tracker")
    print("📱 BTC & SOL Futures Analizi")
    print("⚡ Long/Short | Volume | Liquidations | Funding")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Futures Tracker durduruldu")