import MetaTrader5 as mt5 pip install pandas
import pandas as pd
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator
from ta.volatility import AverageTrueRange  
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from datetime import datetime
import pytz

# ==============================
# TELEGRAM TOKEN
# ==============================
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

# ==============================
# ACTIVE TRADES
# ==============================
active_trades = {}

# ==============================
# MT5 INIT
# ==============================
if not mt5.initialize():
    print("MT5 initialize failed")
    quit()

# ==============================
# GET DATA
# ==============================
def get_data(symbol, timeframe, n=300):

    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, n)

    if rates is None:
        return pd.DataFrame()

    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')

    return df

# ==============================
# SESSION FILTER
# ==============================
def session_filter():

    utc = datetime.now(pytz.utc)
    hour = utc.hour

    if (7 <= hour <= 16) or (12 <= hour <= 21):
        return True

    return False

# ==============================
# ANALYZE MARKET
# ==============================
def analyze(symbol):

    if not session_filter():
        return "⏳ Market outside London/NY session"

    info = mt5.symbol_info(symbol)

    if info is None:
        return "Symbol not found"

    spread = info.spread

    if spread > 30:
        return f"Spread too high ({spread})"

    data = get_data(symbol, mt5.TIMEFRAME_M5, 200)

    if data.empty:
        return "No data"

    close = data['close']
    high = data['high']
    low = data['low']

    ema20 = EMAIndicator(close, 20).ema_indicator()
    ema50 = EMAIndicator(close, 50).ema_indicator()

    rsi = RSIIndicator(close, 14).rsi()

    atr = AverageTrueRange(high, low, close, 14).average_true_range()

    price = close.iloc[-1]
    ema20_last = ema20.iloc[-1]
    ema50_last = ema50.iloc[-1]
    rsi_last = rsi.iloc[-1]
    atr_last = atr.iloc[-1]

    signal = "NO TRADE"
    sl = "-"
    tp = "-"

    if ema20_last > ema50_last and 40 < rsi_last < 65:

        signal = "BUY"
        sl = price - (1.5 * atr_last)
        tp = price + (3 * atr_last)

    elif ema20_last < ema50_last and 35 < rsi_last < 60:

        signal = "SELL"
        sl = price + (1.5 * atr_last)
        tp = price - (3 * atr_last)

    if signal != "NO TRADE":

        active_trades[symbol] = {
            "type": signal,
            "entry": price
        }

    message = f"""
📊 {symbol}

Signal: {signal}

Entry: {round(price,5)}
SL: {round(sl,5) if sl != '-' else '-'}
TP: {round(tp,5) if tp != '-' else '-'}
"""

    return message

# ==============================
# MONITOR TRADE
# ==============================
def monitor_trade(symbol):

    if symbol not in active_trades:
        return "No active trade"

    trade = active_trades[symbol]

    data = get_data(symbol, mt5.TIMEFRAME_M5, 100)

    close = data['close']

    ema20 = EMAIndicator(close, 20).ema_indicator()
    ema50 = EMAIndicator(close, 50).ema_indicator()

    rsi = RSIIndicator(close, 14).rsi()

    ema20_last = ema20.iloc[-1]
    ema50_last = ema50.iloc[-1]
    rsi_last = rsi.iloc[-1]

    if trade["type"] == "BUY":

        if ema20_last < ema50_last or rsi_last > 70:
            del active_trades[symbol]
            return "⚠ EXIT BUY - Market reversing"

    if trade["type"] == "SELL":

        if ema20_last > ema50_last or rsi_last < 30:
            del active_trades[symbol]
            return "⚠ EXIT SELL - Market reversing"

    return "Trade still valid ✅"

# ==============================
# TELEGRAM COMMANDS
# ==============================
async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text("Use: /signal EURUSD")
        return

    symbol = context.args[0].upper()

    result = analyze(symbol)

    await update.message.reply_text(result)

async def monitor(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text("Use: /monitor EURUSD")
        return

    symbol = context.args[0].upper()

    result = monitor_trade(symbol)

    await update.message.reply_text(result)

# ==============================
# RUN BOT
# ==============================
if __name__ == "__main__":

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("signal", signal))
    app.add_handler(CommandHandler("monitor", monitor))

    print("BOT RUNNING")

    app.run_polling()