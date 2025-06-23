# 📊 Binance Futures Tracker

## 🚀 Özellikler

Real-time Binance Futures takip sistemi:

- **📈 Long/Short Oranları** (BTC & SOL)
- **💸 Funding Rates** (Anlık ve 8h tahmini)
- **📊 24h Hacimler** (USDT bazında)
- **⚡ Likidasyonlar** (Büyük işlem takibi)
- **🎯 Market Sentiment** Analizi
- **📱 Telegram** Bildirimleri

## 📁 Dosya Yapısı

```
futures_takip/
├── futures_tracker.py     # Ana tracker sistemi
├── test_futures.py       # Test scripti
├── start_futures.sh      # Başlatma menüsü
├── requirements.txt      # Python paketleri
└── README.md            # Bu dosya
```

## 🔧 Kurulum

```bash
# 1. Gereksinimler
pip install -r requirements.txt

# 2. Bot token ve chat ID değiştir
# futures_tracker.py ve test_futures.py dosyalarında:
BOT_TOKEN = "sizin_token_iniz"
CHAT_ID = "sizin_chat_id_iniz"

# 3. Test et
python3 test_futures.py

# 4. Başlat
./start_futures.sh
```

## ⚡ Kullanım

### **Kolay Başlatma:**
```bash
./start_futures.sh
```

### **Manuel Komutlar:**
```bash
# Test
python3 test_futures.py

# 15 dakika aralık (varsayılan)
python3 futures_tracker.py

# Özel aralık
python3 -c "
from futures_tracker import FuturesTracker
import asyncio
tracker = FuturesTracker()
asyncio.run(tracker.run_tracker(interval_minutes=30))
"
```

## 📊 Rapor İçeriği

### **BTC & SOL için:**
- 💰 **Anlık Fiyat** ve 24h değişim
- 📈 **Long/Short Oranı** (Trader pozisyonları)
- 💸 **Funding Rate** (Anlık ve 8h tahmini)
- 📊 **24h Hacim** (USDT)
- ⚡ **Büyük İşlemler** (Potansiyel likidasyonlar)

### **Market Sentiment:**
- 🟢 **BULLISH** - Alım fırsatı
- 🔴 **BEARISH** - Satım baskısı
- 🟡 **NEUTRAL** - Kararsız piyasa

## 🎯 Analiz Kriterleri

### **Long/Short Oranı:**
- **L/S > 2.0:** Aşırı Long (Bearish sinyal)
- **L/S < 0.5:** Aşırı Short (Bullish sinyal)

### **Funding Rate:**
- **> 0.1%:** Pahalı Long pozisyon (Bearish)
- **< -0.05%:** Ucuz Long pozisyon (Bullish)

### **Likidasyonlar:**
- **>$100K işlemler** potansiyel likidasyon
- **Yüksek frequency** = Volatilite

## 📱 Telegram Raporu

Her 15 dakikada (veya seçtiğiniz aralıkta) detaylı rapor:

```
📊 FUTURES MARKET REPORT 📊
⏰ 23.06.2024 14:30:15 UTC

🟢 BULLISH Market Sentiment
• 🟢 BTC Negatif Funding Rate

━━━━━━━━ ₿ BTC FUTURES ━━━━━━━━
💰 Fiyat: $67,250 (+2.45%)
📊 24h Hacim: $15.2B
📈 Long/Short Oranı: 1.23
💸 Funding Rate: -0.0234%
⚡ Likidasyonlar: 12 adet
...
```

## 🚀 Hızlı Başlangıç

```bash
cd futures_takip
pip install -r requirements.txt
# Token değiştir
python3 test_futures.py
./start_futures.sh
```

**Futures piyasasını takip etmeye başlayın! 💹**