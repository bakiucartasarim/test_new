#!/usr/bin/env python3
"""
Futures Tracker Test Script
"""

import asyncio
from futures_tracker import FuturesTracker

async def test_futures_tracker():
    """Test futures tracker functionality"""
    print("🧪 Futures Tracker Test Başlatılıyor...")
    
    tracker = FuturesTracker()
    
    # Test individual components
    print("\n📊 BTC Long/Short Ratio test...")
    btc_ls = tracker.get_long_short_ratio('BTCUSDT')
    if btc_ls:
        print(f"✅ BTC L/S Ratio: {btc_ls['ratio']:.2f}")
    else:
        print("❌ BTC L/S Ratio başarısız")
    
    print("\n💸 BTC Funding Rate test...")
    btc_funding = tracker.get_funding_rate('BTCUSDT')
    if btc_funding:
        print(f"✅ BTC Funding: {btc_funding['rate']:+.4f}%")
    else:
        print("❌ BTC Funding başarısız")
    
    print("\n📈 SOL Volume test...")
    sol_volume = tracker.get_volume_data('SOL/USDT')
    if sol_volume:
        print(f"✅ SOL Volume: ${tracker.format_number(sol_volume['volume_24h'])}")
    else:
        print("❌ SOL Volume başarısız")
    
    print("\n⚡ BTC Liquidations test...")
    btc_liq = tracker.get_liquidations('BTC/USDT')
    if btc_liq:
        print(f"✅ BTC Large Trades: {btc_liq['large_trades_count']} adet")
    else:
        print("❌ BTC Liquidations başarısız")
    
    # Test full report
    print("\n📊 Full Report Test...")
    report = await tracker.create_futures_report()
    
    # Send test report
    success = await tracker.send_message(report)
    if success:
        print("✅ Test raporu Telegram'a gönderildi!")
    else:
        print("❌ Test raporu gönderilemedi!")
    
    print("\n🎯 Test tamamlandı!")

if __name__ == "__main__":
    asyncio.run(test_futures_tracker())