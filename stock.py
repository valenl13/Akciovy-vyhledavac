# stock.py
import yfinance as yf
import matplotlib.pyplot as plt
import os

class Stock:
    def __init__(self, ticker: str):
        self.ticker = ticker.upper()
        self.data = yf.Ticker(self.ticker)

    def get_info(self):
        info = self.data.info
        return {
            "Název": info.get("shortName", "Neznámý"),
            "Ticker": self.ticker,
            "Odvětví": info.get("industry", "N/A"),
            "Aktuální cena": info.get("currentPrice", "N/A"),
            "Změna (%)": round(info.get("regularMarketChangePercent", 0), 2),
            "Měna": info.get("currency", "N/A"),
            "Burza": info.get("exchange", "N/A")
        }

    def create_price_chart(self, period="1mo", filename="static/chart.png"):
        interval_map = {
        "1d": "5m",     # pro 1 den: 5 minut
        "5d": "15m",    # pro 5 dní: 15 minut
        "1mo": "1d",
        "3mo": "1d",
        "6mo": "1d",
        "1y": "1d"
        }
        interval = interval_map.get(period, "1d")

        hist = self.data.history(period=period, interval=interval)
        if hist.empty:
            print(f"[WARN] Žádná data pro {self.ticker} při periodě {period} a intervalu {interval}")
            return None

        plt.figure(figsize=(10, 5))
        plt.plot(hist.index, hist["Close"], label="Závěrečná cena", color="blue")
        plt.title(f"Vývoj ceny {self.ticker} za období: {period}")
        plt.xlabel("Datum")
        plt.ylabel("Cena")
        plt.grid(True)
        plt.tight_layout()

        os.makedirs("static", exist_ok=True)
        filename = f"static/chart_{self.ticker}_{period}.png"
        plt.savefig(filename)
        plt.close()
        return filename
