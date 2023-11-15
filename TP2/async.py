import aiohttp
import asyncio
import time


async def get_symbols_async():
    url = "https://data-api.binance.vision/api/v3/exchangeInfo"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return [elem["symbol"] for elem in data["symbols"]]


async def get_last_60_candle_info_async(session, symbol, interval):
    url = f"https://data-api.binance.vision/api/v3/klines?symbol={symbol}&interval={interval}"
    async with session.get(url) as response:
        return await response.json()


async def get_last_60_candle_info_all_asset_async(interval):
    async with aiohttp.ClientSession() as session:
        symbols = await get_symbols_async()
        tasks = [get_last_60_candle_info_async(session, symbol, interval) for symbol in symbols]
        return await asyncio.gather(*tasks)


if __name__ == "__main__":
    start = time.time()
    loop = asyncio.get_event_loop()
    candle_info = loop.run_until_complete(get_last_60_candle_info_all_asset_async(interval="1h"))
    print(candle_info)
    end = time.time()
    print(round(end - start, 2), "sec to retrieve the data.")

"""
OUTPUT:
140.42 sec to retrieve the data.
"""