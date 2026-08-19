import os
import time
import requests
import ccxt
from threading import Thread
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Paper Trading Bot is Active and Running 24/7!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

binance = ccxt.binance()

paper_wallet = {
    "USDT": 1000.0,
    "ETH": 0.0,
    "total_profit": 0.0,
    "trades_count": 0
}

def simulate_paper_trade(cex_price, dex_price, spread):
    global paper_wallet
    trade_amount_usdt = 100.0
    
    if paper_wallet["USDT"] < trade_amount_usdt:
        print("⚠️ Paper Trading Alert: Low Balance to execute trade.")
        return

    if cex_price < dex_price:
        buy_price = cex_price
        sell_price = dex_price
        buy_venue = "Binance"
        sell_venue = "Uniswap V3"
    else:
        buy_price = dex_price
        sell_price = cex_price
        buy_venue = "Uniswap V3"
        sell_venue = "Binance"

    eth_bought = trade_amount_usdt / buy_price
    gross_sell_value = eth_bought * sell_price
    est_fees = (trade_amount_usdt + gross_sell_value) * 0.002
    net_profit = (gross_sell_value - trade_amount_usdt) - est_fees

    if net_profit > 0:
        paper_wallet["USDT"] += net_profit
        paper_wallet["total_profit"] += net_profit
        paper_wallet["trades_count"] += 1

        print("==================================================")
        print(f"🚀 [PAPER TRADE EXECUTED #{paper_wallet['trades_count']}]")
        print(f"🟢 Buy on {buy_venue} @ ${buy_price:.2f}")
        print(f"🔴 Sell on {sell_venue} @ ${sell_price:.2f}")
        print(f"💰 Net Profit (after fees): +${net_profit:.4f} USDT")
        print(f"📊 New Paper Balance: ${paper_wallet['USDT']:.2f} USDT")
        print("==================================================")

def track_arbitrage():
    print("🤖 Starting Arbitrage Paper-Trading Bot...")
    print(f"💼 Initial Balance: ${paper_wallet['USDT']} USDT")
    
    while True:
        try:
            ticker = binance.fetch_ticker('ETH/USDT')
            cex_price = ticker['last']

            dex_url = "https://api.dexscreener.com/latest/dex/pairs/ethereum/0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640"
            response = requests.get(dex_url).json()
            dex_price = float(response['pair']['priceUsd'])

            spread = abs(cex_price - dex_price) / cex_price * 100

            print(f"Binance: ${cex_price:.2f} | Uniswap: ${dex_price:.2f} | Spread: {spread:.2f}%")

            if spread >= 0.5:
                print(f"⚡ Opportunity Detected! Spread: {spread:.2f}%")
                simulate_paper_trade(cex_price, dex_price, spread)

        except Exception as e:
            print(f"Error fetching prices: {e}")

        time.sleep(10)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    track_arbitrage()
