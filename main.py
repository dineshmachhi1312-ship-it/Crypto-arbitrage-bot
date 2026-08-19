import os
import time
import requests
import ccxt
from threading import Thread
from flask import Flask

# Flask server for Render Port Binding
app = Flask(__name__)

@app.route('/')
def home():
    return "Arbitrage Bot is Running 24/7!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# Binance Setup
binance = ccxt.binance()

# Arbitrage Monitoring Loop
def track_arbitrage():
    print("Starting Arbitrage Monitoring...")
    while True:
        try:
            # Binance ETH/USDT
            ticker = binance.fetch_ticker('ETH/USDT')
            cex_price = ticker['last']

            # DexScreener Uniswap V3 ETH/USDT
            dex_url = "https://api.dexscreener.com/latest/dex/pairs/ethereum/0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640"
            response = requests.get(dex_url).json()
            dex_price = float(response['pair']['priceUsd'])

            # Spread Calculation
            spread = abs(cex_price - dex_price) / cex_price * 100

            print(f"Binance: ${cex_price:.2f} | Uniswap V3: ${dex_price:.2f} | Spread: {spread:.2f}%")

            if spread >= 0.8:
                print(f"🔥 ARBITRAGE OPPORTUNITY FOUND! Spread: {spread:.2f}% 🔥")

        except Exception as e:
            print(f"Error fetching prices: {e}")

        time.sleep(10)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    track_arbitrage()
