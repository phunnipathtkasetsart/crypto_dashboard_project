
import requests

# ---------------- MARKET OVERVIEW ---------------- #

def get_market_overview():
    url = "https://api.coingecko.com/api/v3/global"
    data = requests.get(url, timeout=10).json()["data"]

    return {
        "btc_dominance": f"{data['market_cap_percentage']['btc']:.2f}%",
        "market_cap": f"${data['total_market_cap']['usd']/1e12:.2f}T",
        "market_change": f"{data['market_cap_change_percentage_24h_usd']:.2f}%"
    }


# ---------------- TOP MOVERS ---------------- #

def get_top_movers(limit=5):
    url = "https://api.binance.com/api/v3/ticker/24hr"
    tickers = requests.get(url, timeout=10).json()

    usdt_pairs = [
        t for t in tickers
        if t["symbol"].endswith("USDT")
    ]

    sorted_pairs = sorted(
        usdt_pairs,
        key=lambda x: float(x["priceChangePercent"]),
        reverse=True
    )

    gainers = sorted_pairs[:limit]
    losers = sorted_pairs[-limit:][::-1]

    return gainers, losers


# ---------------- CRYPTO NEWS ---------------- #

def get_crypto_news(limit=5):
    url = "https://cryptopanic.com/api/v1/posts/?auth_token=&public=true"
    data = requests.get(url, timeout=10).json()

    return [
        post["title"]
        for post in data["results"][:limit]
    ]
