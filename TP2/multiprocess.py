import requests
import multiprocessing
import time
from main import get_symbols


def get_last_60_candle_info_process(symbol, interval, output):
    url = f"https://data-api.binance.vision/api/v3/klines?symbol={symbol}&interval={interval}"
    response = requests.get(url)
    output.put({symbol: response.json()})


def get_last_60_candle_info_all_asset_process(interval):
    output = multiprocessing.Queue()
    symbols = get_symbols()
    processes = []
    for symbol in symbols:
        process = multiprocessing.Process(target=get_last_60_candle_info_process, args=(symbol, interval, output))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()
    result = {}
    while not output.empty():
        result.update(output.get())
    return result


if __name__ == "__main__":
    start = time.time()
    candle_info = get_last_60_candle_info_all_asset_process(interval="1h")
    print(candle_info)
    end = time.time()
    print(round(end - start, 2), "sec to retrieve the data.")

"""
OUTPUT:
XXX sec to retrieve the data. OUT OF TIME...
"""