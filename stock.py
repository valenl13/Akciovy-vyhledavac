# stock.py
import yfinance as yf
import matplotlib.pyplot as plt
import os
from abc import ABC, abstractmethod

class Asset(ABC):
    def __init__(self, ticker):
        self.ticker = ticker.upper()

    @abstractmethod
    def get_price(self):
        pass

    @abstractmethod
    def create_price_chart(self, period="1mo"):
        pass

class Stock(Asset):
    popular_tickers = ["AAPL", "MSFT", "TSLA", "GOOGL"]

    def __init__(self, ticker):
        super().__init__(ticker)
        self.data = yf.Ticker(self.ticker)

    def get_price(self):
        return self.data.info.get("regularMarketPrice")
    
    def get_info(self):
        info = self.data.info
        return {
            "Název": info.get("shortName", "Neznámý"),
            "Odvětví": info.get("industry", "N/A"),
            "Aktuální cena": info.get("currentPrice", "N/A"),
            "Změna (%)": round(info.get("regularMarketChangePercent", 0), 2),
            "Měna": info.get("currency", "N/A"),
            "Burza": info.get("exchange", "N/A")
        }

    def create_price_chart(self, period="1mo"):
        interval_map = {
            "1d": "5m", "5d": "15m", "1mo": "1d", "3mo": "1d",
            "6mo": "1d", "1y": "1d", "2y": "1wk", "5y": "1wk", "10y": "1mo"
        }
        interval = interval_map.get(period, "1d")
        hist = self.data.history(period=period, interval=interval)

        if hist.empty:
            print(f"[WARN] Žádná data pro {self.ticker} při periodě {period}")
            return None

        plt.figure(figsize=(10, 5))
        plt.plot(hist.index, hist["Close"], label="Cena", color="blue")
        plt.title(f"{self.ticker} – vývoj za {period}")
        plt.xlabel("Datum")
        plt.ylabel("Cena")
        plt.grid(True)
        plt.tight_layout()

        os.makedirs("static", exist_ok=True)
        filename = f"static/chart_{self.ticker}_{period}.png"
        plt.savefig(filename)
        plt.close()
        return filename
