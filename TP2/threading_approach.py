import requests
import threading
import time
from main import get_symbols


def get_last_60_candle_info_thread(symbol, interval, result):
    url = f"https://data-api.binance.vision/api/v3/klines?symbol={symbol}&interval={interval}"
    response = requests.get(url)
    result[symbol] = response.json()


def get_last_60_candle_info_all_asset_thread(interval):
    result = {}
    symbols = get_symbols()
    threads = []
    for symbol in symbols:
        thread = threading.Thread(target=get_last_60_candle_info_thread, args=(symbol, interval, result))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    return result


if __name__ == "__main__":
    start = time.time()
    candle_info = get_last_60_candle_info_all_asset_thread(interval="1h")
    print(candle_info)
    end = time.time()
    print(round(end - start, 2), "sec to retrieve the data.")

"""
OUTPUT:
246.83 sec to retrieve the data.
"""
