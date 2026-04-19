# 🤖 Trading Signal Bot (MT5 + Telegram)

An automated trading signal bot built with **Python**, integrated with **MetaTrader 5** and **Telegram**, designed to analyze the market using technical indicators and deliver real-time trading signals.

---

## 📌 Overview

This project combines algorithmic trading logic with messaging automation to provide:

* 📊 Real-time market analysis
* 📩 Telegram signal notifications
* 📈 Technical indicator-based strategy
* 🔁 Trade monitoring system

---

## ⚙️ Features

* EMA 20 / EMA 50 trend detection
* RSI momentum filtering
* ATR-based Stop Loss & Take Profit
* Spread filtering (avoid bad entries)
* London & New York session filter
* Active trade tracking
* Telegram bot commands

---

## 🧠 Strategy Logic

The bot uses a combination of:

* **Trend** → EMA crossover
* **Momentum** → RSI levels
* **Volatility** → ATR for SL/TP

### Buy Conditions

* EMA20 > EMA50
* RSI between 40–65

### Sell Conditions

* EMA20 < EMA50
* RSI between 35–60

---

## 💬 Telegram Commands

| Command           | Description          |
| ----------------- | -------------------- |
| `/signal EURUSD`  | Get a trading signal |
| `/monitor EURUSD` | Check active trade   |

---

## 📁 Project Structure

```id="0j3n9s"
trading-bot/
│
├── bot.py              # Main bot file
├── requirements.txt    # Dependencies
├── .env                # Secret keys (DO NOT SHARE)
```

---

## 🔐 Environment Variables

Create a `.env` file:

```env id="l3u6xq"
TELEGRAM_TOKEN=your_token_here
```

---

## 🛠️ Installation

```bash id="w0q7p2"
git clone https://github.com/your-username/trading-bot.git
cd trading-bot
pip install -r requirements.txt
```

---

## ▶️ Run the Bot

```bash id="z6u9sx"
python bot.py
```

---

## 📦 Requirements

* Python 3.9+
* MetaTrader 5 installed & running
* MT5 account connected

Libraries:

* MetaTrader5
* pandas
* ta
* python-telegram-bot
* pytz

---

## ⚠️ Disclaimer

This project is for **educational purposes only**.
Trading involves risk. Use this bot at your own responsibility.

---

## 🚀 Future Improvements

* 📊 Multi-timeframe confirmation
* 🤖 Smart AI-based signals
* 📱 Web dashboard
* 🔔 Auto trade execution
* 📉 Backtesting system

---

## 👨‍💻 Author

**Souhail**
GitHub: https://github.com/SOUH4IL-dev

---

## ⭐ Support

If you like this project, consider giving it a ⭐ on GitHub.
