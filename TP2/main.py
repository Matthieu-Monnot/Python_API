import requests
import time


def get_symbols():
    url = "https://data-api.binance.vision/api/v3/exchangeInfo"
    response = requests.get(url)
    ls_vol = response.json()["symbols"]
    return [elem["symbol"] for elem in ls_vol]


def get_last_60_candle_info(symbol, interval):
    url = f"https://data-api.binance.vision/api/v3/klines?symbol={symbol}&interval={interval}"
    response = requests.get(url)
    ls_vol = response.json()
    return ls_vol


def get_last_60_candle_info_all_asset(interval):
    all_infos = []
    assets = get_symbols()
    for asset in assets:
        all_infos.append(get_last_60_candle_info(asset, interval))
    return all_infos


if __name__ == "__main__":
    start = time.time()
    print(get_last_60_candle_info_all_asset(interval="1h"))
    end = time.time()
    print(round(end - start, 2), "sec to retrieve the data.")

"""
OUTPUT:
XXX sec to retrieve the data. OUT OF TIME...
"""