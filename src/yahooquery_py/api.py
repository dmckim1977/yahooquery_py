import logging
from datetime import datetime

from yahooquery import Ticker

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
    dt = datetime.strptime(date, "%Y-%m-%d").date()
    return _close_price(yahoo_symbol, date, dt)


def _close_price(yahoo_symbol, date: str, dt: datetime) -> float:
    try:
        df = Ticker(yahoo_symbol).history(period="5d", interval="30m", start=date)
        df.reset_index(inplace=True)
    except Exception as e:
        logging.error(f"Error for {yahoo_symbol} and date {date}: {e}")

    if not len(df) == 0:
        try:
            df.set_index("date", inplace=True)
        except Exception as e:
            logging.error(f"Error for {yahoo_symbol} and date {date}: {e}")

        try:
            close_price = df.between_time("15:59:59", "16:02:00")['close'].item()
            if isinstance(close_price, float):
                return close_price
            else:
                logging.error(f"Close price {close_price} is not a float")
        except Exception as e:
            logging.error(f"Error for {yahoo_symbol} and date {date}: {e}")


if __name__ == "__main__":
    c = daily_close("aapl", "2024-10-18")
    print(type(c),c)

    # spx = Ticker("^SPX")
    # spx_hist = spx.history(period="5d", interval="1d")
    # print(f"SPX {spx_hist.columns}")
    #
    # es = Ticker("ES=F")
    # es_hist = es.history(period="5d", interval="1d")
    # print(f"ES {es_hist.columns}")
    #
    # aapl = Ticker("AAPL")
    # aapl_hist = aapl.history(period="5d", interval="1d")
    # print(f"ES {aapl_hist.columns}")
