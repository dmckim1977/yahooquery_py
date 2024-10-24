import logging
from datetime import datetime

import pandas as pd
import yfinance as yf

futures = [
    ["ES", "ES=F", "ES1!", "/ES:XCME"],
    ["NQ", "NQ=F", "NQ1!", "/NQ:XCME"],
    ["RTY", "RTY=F", "RTY1!", "/RTY:XCME"],
]

symbol_mapper = {
    "ES": "ES=F",
    "NQ": "NQ=F",
    "NQ1!": "NQ=F",
    "RTY": "RTY=F",
    "SPX": "^SPX",
    "RUT": "^RUT",
    "NDX": "^NDX"
}

def map_symbol(symbol: str) -> str:
    return symbol_mapper.get(symbol.upper(), symbol)


def daily_close(symbol: str, date: str) -> float:
    yahoo_symbol = map_symbol(symbol)

    # Create a Ticker object
    ticker = yf.Ticker(yahoo_symbol)

    # Fetch the historical data for the specific date
    historical_data = ticker.history(start=date)

    # Get the closing price
    if not historical_data.empty:
        return float(historical_data['Close'].iloc[0])
    else:
        logging.error(f"No data available for {yahoo_symbol} on {date}.")



if __name__ == "__main__":
    c = daily_close("ES", "2024-10-01")
    print(type(c),c)

    # spx = Ticker("^SPX")
    # spx_hist = spx.history(period="5d", interval="1d")
    # print(f"SPX {spx_hist.columns}")
    #
    # es = Ticker("ES=F")
    # es_hist = es.history(period="5d", interval="1d")
    # print(f"ES {es_hist}")
    #
    # aapl = Ticker("AAPL")
    # aapl_hist = aapl.history(period="5d", interval="1d")
    # print(f"ES {aapl_hist.columns}")
