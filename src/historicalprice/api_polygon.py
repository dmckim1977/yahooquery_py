import logging
import os
from datetime import datetime, timedelta
from typing import Dict, Optional

import httpx
from dotenv import load_dotenv

load_dotenv()


def polygon_request(url: str, params: Optional[Dict[str, str]] = None, retries=3) -> httpx.Response:
    """
    Makes a http request and checks for a successful response. Retries x times if its a bad request.

    :param url: Prepared request
    :param params:
    :param retries:
    :return:
    """
    transport = httpx.HTTPTransport(retries=3)
    with httpx.Client(transport=transport) as client:
        try:
            return client.get(url, params=params if params else {}).raise_for_status().json()
        except httpx.HTTPStatusError as exc:
            logging.error(f'Error response {exc.response.status_code} while requesting {exc.request.url!r}.')
        except Exception as e:
            logging.error(f'Error while requesting {url!r}: {e}')
        finally:
            client.close()


def handle_datetime(date: datetime) -> str:
    if isinstance(date, str):
        return date
    else:
        try:
            return date.strftime("%Y-%m-%d")
        except Exception as e:
            logging.error(f"Failed converting date: {date} with error: {e}")


def index_eod_ohlc(symbol: str, date: datetime | str) -> Dict:
    """
    Returns the OHLC for an index for one day.

    :param symbol: formats URL to include `I:` before the symbol.
    :param date: Needs a datetime format `YYYY-MM-DD` but function will convert datetime.
    :return:

    ohlc = index_eod_ohlc('spx', datetime.today())
    print(ohlc)

    {'symbol': 'SPX', 'open': 5817.8, 'high': 5817.8, 'low': 5784.92, 'close': 5809.86}

    """
    keys_list = ['symbol', 'open', 'high', 'low', 'close']
    url = (f"https://api.polygon.io/v1/open-close/I:{symbol.upper()}/{handle_datetime(date)}")

    try:
        res = polygon_request(url, params={'apiKey': os.getenv('POLYGON_API')})

        # Filter to only the needed keys
        filtered_res = {k: v for k,v in res.items() if k in keys_list}

        # Clean the symbol, specific for indexes
        filtered_res['symbol'] = filtered_res['symbol'].split(':')[1]
        return filtered_res

    except Exception as e:
        logging.error(f"Failed getting response: {date} with error: {e}")


def index_eod_close(symbol: str, date: datetime | str) -> float:
    """
    Returns the close of an index for one day.

    :param symbol: formats URL to include `I:` before the symbol.
    :param date: Needs a datetime format `YYYY-MM-DD` but function will convert datetime.
    :return:

    o = index_eod_close('spx', datetime.today())
    print(type(o), o)

    <class 'float'> 5809.86

    """
    ohlc = index_eod_ohlc(symbol, date)
    return float(ohlc['close'])


def stock_eod_ohlcv(symbol: str, date: datetime | str) -> Dict:
    """
    Queries the OHLC for one day.

    :param symbol:
    :param date: Needs a datetime format `YYYY-MM-DD` but function will convert datetime.
    :return: dict

    :example:

    aapl = stock_eod_ohlcv('aapl', datetime.today())
    print(aapl)

    {'symbol': 'AAPL', 'open': 229.98, 'high': 230.82, 'low': 228.41, 'close': 230.57, 'volume': 28835824.0}
    """
    keys_list = ['symbol', 'open', 'high', 'low', 'close', 'volume']
    url = (f"https://api.polygon.io/v1/open-close/{symbol.upper()}/{handle_datetime(date)}")

    try:
        res = polygon_request(url, params={'apiKey': os.getenv('POLYGON_API'), 'adjusted': True})

        # Filter to only the needed keys
        filtered_res = {k: v for k,v in res.items() if k in keys_list}

        return filtered_res

    except Exception as e:
        logging.error(f"Failed getting response: {date} with error: {e}")


def stock_eod_close(symbol: str, date: datetime | str) -> float:
    """
    Queries the regular session close price for one day.
    :param symbol:
    :param date: Needs a datetime format `YYYY-MM-DD` but function will convert datetime.
    :return:

    aapl = stock_eod_close('aapl', datetime.today())
    print(type(aapl), aapl)

    <class 'float'> 230.57
    """
    ohlc = stock_eod_ohlcv(symbol, date)
    return float(ohlc['close'])


if __name__ == "__main__":
    # print(handle_datetime(datetime.now()))

    ohlc = index_eod_ohlc('spx', datetime.today())
    print(ohlc)

    o = index_eod_close('spx', datetime.today())
    print(type(o), o)

    # aapl = stock_eod_ohlcv('aapl', datetime.today())
    # print(aapl)

    # aapl = stock_eod_close('aapl', datetime.today())
    # print(type(aapl), aapl)