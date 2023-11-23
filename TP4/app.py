from fastapi import FastAPI
from collections import Counter
import requests


app = FastAPI()
rate_limiting = Counter()
route_last_access = {}


def get_binance_candlestick_data(symbol, interval='1m', limit=60):
    url = f'https://api.binance.com/api/v3/klines'
    params = {'symbol': symbol, 'interval': interval, 'limit': limit}
    response = requests.get(url, params=params)
    response.raise_for_status()
    klines = response.json()
    return klines


def get_binance_trade_volume(symbol, limit=500):
    url = f'https://api.binance.com/api/v3/trades'
    params = {'symbol': symbol, 'limit': limit}
    response = requests.get(url, params=params)
    response.raise_for_status()
    trades = response.json()
    return trades


def calculate_rsi(data, period=14):
    closes = [float(trade['price']) for trade in data]
    changes = [closes[i] - closes[i - 1] for i in range(1, len(closes))]
    gains = [change if change > 0 else 0 for change in changes]
    losses = [-change if change < 0 else 0 for change in changes]
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    for i in range(period, len(closes)):
        current_gain = gains[i - 1] if gains[i - 1] > 0 else 0
        current_loss = losses[i - 1] if losses[i - 1] > 0 else 0
        avg_gain = (avg_gain * (period - 1) + current_gain) / period
        avg_loss = (avg_loss * (period - 1) + current_loss) / period
    if avg_loss == 0:
        return 100
    else:
        relative_strength = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + relative_strength))
        return rsi


def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    closes = [float(trade['price']) for trade in data]
    short_ema = sum(closes[-short_window:]) / short_window
    long_ema = sum(closes[-long_window:]) / long_window
    macd_line = short_ema - long_ema
    signal_line = sum(closes[-signal_window:]) / signal_window
    return macd_line, signal_line


@app.get("/rendement")
def get_rendement(symbol):
    klines = get_binance_candlestick_data(symbol=symbol)
    last_candle = klines[-1]
    open_price = float(last_candle[1])
    close_price = float(last_candle[4])
    returns = ((close_price - open_price) / open_price) * 100
    return returns


@app.get("/moneyflowclassique")
def get_moneyflowclassique(symbol):
    trades = get_binance_trade_volume(symbol=symbol)
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
    return money_flow_classique


@app.get("/rsi")
def get_rsi(symbol):
    trades = get_binance_trade_volume(symbol=symbol)
    if trades is None or len(trades) < 15:
        return None
    rsi_value = calculate_rsi(trades)
    return rsi_value


@app.get("/macd")
def get_macd(symbol):
    trades = get_binance_trade_volume(symbol=symbol)
    if trades is None or len(trades) < 26:
        return None
    macd_value, signal_value = calculate_macd(trades)
    return macd_value, signal_value


"""
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    route = request.url.path
    if route not in route_last_access:
        route_last_access[route] = datetime.utcnow()
    time_difference = datetime.utcnow() - route_last_access[route]
    if time_difference < timedelta(minutes=0.1):
        if route_last_access[route] > datetime.utcnow() - timedelta(seconds=30) and route_last_access[route] != datetime.min:
            raise HTTPException(status_code=400, detail="Rate limit exceeded. Try again later.")
    route_last_access[route] = datetime.utcnow()
    response = await call_next(request)
    return response
"""
