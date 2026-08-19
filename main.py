import time
import ccxt
import requests

print("Starting DEX vs CEX Arbitrage Monitor...")

# CEX setup (Binance)
cex = ccxt.binance()
cex_symbol = 'ETH/USDT'

# DEX setup (Uniswap V3 via DexScreener API)
dex_api_url = "https://api.dexscreener.com/latest/dex/pairs/ethereum/0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640"

while True:
    try:
        # 1. Get CEX Price
        cex_ticker = cex.fetch_ticker(cex_symbol)
        cex_price = float(cex_ticker['last'])

        # 2. Get DEX Price
        response = requests.get(dex_api_url, timeout=5)
        dex_data = response.json()
        dex_price = float(dex_data['pair']['priceUsd'])

        print(f"[CEX - Binance] ETH: ${cex_price:.2f} | [DEX - Uniswap] ETH: ${dex_price:.2f}")

        # 3. Calculate Price Gap
        diff = abs(cex_price - dex_price)
        spread_pct = (diff / min(cex_price, dex_price)) * 100

        print(f"Spread: ${diff:.2f} ({spread_pct:.2f}%)")

        if spread_pct > 0.8:  # 0.8% threshold
            print(">>> DEX vs CEX ARBITRAGE OPPORTUNITY FOUND! <<<\n")
        else:
            print("No significant gap.\n")

    except Exception as e:
        print(f"Error fetching prices: {e}")

    time.sleep(10)
