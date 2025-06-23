#!/bin/bash

# Futures Tracker Starter Script

echo "📊 Binance Futures Tracker"
echo "=========================="

# Stop any existing tracker
echo "🔄 Mevcut tracker'ı durduruyor..."
pkill -f futures_tracker.py 2>/dev/null
sleep 2

echo ""
echo "Hangi modu çalıştırmak istiyorsunuz?"
echo ""
echo "1) Test Modu (Bir kez rapor gönder)"
echo "2) Sürekli Takip - 15 dakika aralık"
echo "3) Sürekli Takip - 30 dakika aralık" 
echo "4) Sürekli Takip - 1 saat aralık"
echo "5) Özel Aralık"
echo ""
read -p "Seçiminizi yapın (1-5): " choice

case $choice in
    1)
        echo "🧪 Test modu başlatılıyor..."
        python3 test_futures.py
        ;;
    2)
        echo "📊 15 dakika futures takip başlatılıyor..."
        python3 futures_tracker.py
        ;;
    3)
        echo "📊 30 dakika futures takip başlatılıyor..."
        python3 -c "
import asyncio
from futures_tracker import FuturesTracker
tracker = FuturesTracker()
asyncio.run(tracker.run_tracker(interval_minutes=30))
"
        ;;
    4)
        echo "📊 1 saat futures takip başlatılıyor..."
        python3 -c "
import asyncio
from futures_tracker import FuturesTracker
tracker = FuturesTracker()
asyncio.run(tracker.run_tracker(interval_minutes=60))
"
        ;;
    5)
        read -p "Kaç dakika aralık istiyorsunuz? " interval
        echo "📊 $interval dakika futures takip başlatılıyor..."
        python3 -c "
import asyncio
from futures_tracker import FuturesTracker
tracker = FuturesTracker()
asyncio.run(tracker.run_tracker(interval_minutes=$interval))
"
        ;;
    *)
        echo "❌ Geçersiz seçim!"
        exit 1
        ;;
esac