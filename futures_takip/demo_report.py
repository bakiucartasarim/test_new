#!/usr/bin/env python3
"""
Demo Futures Report - Manual Test
"""

import asyncio
from futures_tracker import FuturesTracker

async def create_demo_report():
    """Create one demo report and send it"""
    print("📊 Demo Futures Report oluşturuluyor...")
    
    tracker = FuturesTracker()
    
    # Create one report
    report = await tracker.create_futures_report()
    
    print("✅ Rapor oluşturuldu!")
    print("📱 Telegram'a gönderiliyor...")
    
    # Send report
    success = await tracker.send_message(report)
    
    if success:
        print("✅ Demo rapor başarıyla gönderildi!")
        print("🚀 Ana sistem çalıştırmaya hazır!")
    else:
        print("❌ Demo rapor gönderilemedi")
    
    print("\n📊 Rapor içeriği:")
    print("-" * 50)
    print(report[:500] + "..." if len(report) > 500 else report)

if __name__ == "__main__":
    asyncio.run(create_demo_report())