import os
from concurrent import futures
import grpc
import taskmanager_pb2
import taskm_pb2_grpc
import requests
from datetime import datetime, timedelta
import pickle
import time
import threading


def get_binance_trade_volume(symbol, limit=500):
    url = f'https://api.binance.com/api/v3/trades'
    params = {'symbol': symbol, 'limit': limit}
    response = requests.get(url, params=params)
    response.raise_for_status()
    trades = response.json()
    return trades


def get_binance_trade_volume_2(symbol, hours=1):
    url = f'https://api.binance.com/api/v3/trades'
    params = {'symbol': symbol, 'limit': 1000}
    response = requests.get(url, params=params)
    response.raise_for_status()
    trades = response.json()
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)
    filtered_trades = [trade for trade in trades if start_time <= datetime.utcfromtimestamp(int(trade['time']) / 1000) <= end_time]
    return filtered_trades


def get_binance_candlestick_data(symbol, interval='1m', limit=60):
    url = f'https://api.binance.com/api/v3/klines'
    params = {'symbol': symbol, 'interval': interval, 'limit': limit}
    response = requests.get(url, params=params)
    response.raise_for_status()
    klines = response.json()
    return klines

def load_cache(file_path):
    try:
        with open(file_path, 'rb') as f:
            cached_data = pickle.load(f)
            data, timestamp = cached_data
            return data, timestamp
    except (FileNotFoundError, pickle.UnpicklingError):
        return None

def save_cache(file_path, data):
    timestamp = time.localtime().tm_min
    print("Data save at ", timestamp)
    with open(file_path, 'wb') as f:
        pickle.dump((data, timestamp), f)



class TaskService(taskm_pb2_grpc.TaskServiceServicer):
    def __init__(self):
        self.cache_dir = "cache_directory"
        self.last_cache_timestamp = 0
        self.update_market_data_cache()
        self.cache_update_thread = threading.Thread(target=self.update_cache_periodically)
        self.cache_update_thread.daemon = True
        self.cache_update_thread.start()

    def update_cache_periodically(self):
        while True:
            # Mettez à jour le cache toutes les heures (3600 secondes)
            time.sleep(60)
            self.update_market_data_cache()

    def update_market_data_cache(self):
        cache_key = f"mfC_BTCUSDT"
        trades = get_binance_trade_volume("BTCUSDT")
        if trades is not None:
            self.save_to_cache(cache_key, trades)

        cache_key = f"mfT_BTCUSDT"
        trades = get_binance_trade_volume_2("BTCUSDT")
        if trades is not None:
            self.save_to_cache(cache_key, trades)

        cache_key = f"rend_BTCUSDT"
        klines = get_binance_candlestick_data("BTCUSDT")
        if klines is not None:
            self.save_to_cache(cache_key, klines)

        cache_key = f"vwap_BTCUSDT"
        trades = get_binance_trade_volume_2("BTCUSDT")
        if trades is not None:
            self.save_to_cache(cache_key, trades)

        cache_key = f"Twap_BTCUSDT"
        klines = get_binance_candlestick_data("BTCUSDT")
        if trades is not None:
            self.save_to_cache(cache_key, klines)

    def load_from_cache(self, cache_key):
        cache_path = os.path.join(self.cache_dir, f"{cache_key}.pkl")
        cached_data=load_cache(cache_path)
        if cached_data is not None and len(cached_data) == 2:
            return cached_data
        else:
            return None, None


    def save_to_cache(self, cache_key, data):
        cache_path = os.path.join(self.cache_dir, f"{cache_key}.pkl")
        save_cache(cache_path, data)

    def MoneyFlowClassique(self, request, context):
        cache_key = f"mfC_BTCUSDT"
        cached_data, timestamp = self.load_from_cache(cache_key)
        #current_hour = time.localtime().tm_hour
        current_hour = time.localtime().tm_min

        if cached_data is None or current_hour > timestamp:
            trades = get_binance_trade_volume("BTCUSDT")
            self.save_to_cache(cache_key, trades)
        else:
            trades = cached_data

        if trades is None:
            return None


        volume_taker_buyer = 0
        volume_taker_seller = 0
        for trade in trades:
            if isinstance(trade, dict):

                if trade.get('isBuyerMaker'):
                    volume_taker_seller += float(trade['qty'])
                else:
                    volume_taker_buyer += float(trade['qty'])
        if volume_taker_seller == 0:
            money_flow_classique = None
        else:
            money_flow_classique = volume_taker_buyer / volume_taker_seller

        return taskmanager_pb2.MoneyFlowClassiqueResponse(value=money_flow_classique)

    def MoneyFlowTempore(self, request, context):
        cache_key = f"mfT_BTCUSDT"
        cached_data, timestamp = self.load_from_cache(cache_key)
        # current_hour = time.localtime().tm_hour
        current_hour = time.localtime().tm_min

        if cached_data is None or current_hour > timestamp:
            trades = get_binance_trade_volume_2("BTCUSDT")
            self.save_to_cache(cache_key, trades)
        else:
            trades = cached_data

        if trades is None:
            return None
        minutes_taker_buyer_greater = 0
        for trade in trades:
            if trade['isBuyerMaker']:
                minutes_taker_buyer_greater += 1
        money_flow_temporel = minutes_taker_buyer_greater / 60
        return taskmanager_pb2.MoneyFlowTemporeResponse(value=money_flow_temporel)

    def Rendement(self, request, context):
        cache_key = f"rend_BTCUSDT"
        cached_data, timestamp = self.load_from_cache(cache_key)
        # current_hour = time.localtime().tm_hour
        current_hour = time.localtime().tm_min

        if cached_data is None or current_hour > timestamp:
            klines = get_binance_candlestick_data("BTCUSDT")
            self.save_to_cache(cache_key, klines)
        else:
            klines = cached_data


        if klines is None:
            return None
        last_candle = klines[-1]
        open_price = float(last_candle[1])
        close_price = float(last_candle[4])
        returns = ((close_price - open_price) / open_price) * 100
        return taskmanager_pb2.RendementResponse(value=returns)

    def Vwap(self, request, context):
        cache_key = f"vwap_BTCUSDT"
        cached_data, timestamp = self.load_from_cache(cache_key)
        # current_hour = time.localtime().tm_hour
        current_hour = time.localtime().tm_min

        if cached_data is None or current_hour > timestamp:
            trades = get_binance_trade_volume_2("BTCUSDT")
            self.save_to_cache(cache_key, trades)
        else:
            trades = cached_data


        if trades is None or len(trades) == 0:
            return None
        total_price_volume = 0
        total_volume = 0
        for trade in trades:
            price = float(trade['price'])
            volume = float(trade['qty'])
            total_price_volume += price * volume
            total_volume += volume
        vwap = total_price_volume / total_volume
        return taskmanager_pb2.VwapResponse(value=vwap)

    def Twap(self, request, context):
        cache_key = f"Twap_BTCUSDT"
        cached_data, timestamp = self.load_from_cache(cache_key)
        # current_hour = time.localtime().tm_hour
        current_hour = time.localtime().tm_min

        if cached_data is None or current_hour > timestamp:
            klines = get_binance_candlestick_data("BTCUSDT")
            self.save_to_cache(cache_key, klines)
        else:
            klines = cached_data


        if klines is None:
            return None
        total_close_price = 0
        num_minutes = len(klines)
        for kline in klines:
            close_price = float(kline[4])
            total_close_price += close_price
        twap = total_close_price / num_minutes
        return taskmanager_pb2.TwapResponse(value=twap)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    taskm_pb2_grpc.add_TaskServiceServicer_to_server(TaskService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    cache_dir = "cache_directory"
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    serve()
