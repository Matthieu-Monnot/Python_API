import os
from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, Form
from collections import Counter
import requests
from fastapi.security import OAuth2PasswordRequestForm
import pickle
from Authentification import User, fake_users_db, fake_hash_password, \
    UserInDB, get_current_user, update_user_subscription, save_new_user, delete_user, get_access_moneyflowclassique, \
    get_access_rsi, get_access_macd, get_access_sma

app = FastAPI()
rate_limiting = Counter()
route_last_access = {}
cache_dir = "cache_directory"

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



def load_from_cache(cache_key):
    cache_path = os.path.join(cache_dir, f"{cache_key}.pkl")
    try:
        with open(cache_path, 'rb') as f:
            cached_data = pickle.load(f)
            return cached_data
    except (FileNotFoundError, pickle.UnpicklingError):
        return None



def save_to_cache(cache_key, data):
    cache_path = os.path.join(cache_dir, f"{cache_key}.pkl")
    with open(cache_path, 'wb') as f:
        pickle.dump(data, f)


@app.get("/rendement")
def get_rendement(symbol, loadcash:bool):
    cache_key = f"rend_{symbol}"
    if loadcash:
        return load_from_cache(cache_key)
    klines = get_binance_candlestick_data(symbol=symbol)
    last_candle = klines[-1]
    open_price = float(last_candle[1])
    close_price = float(last_candle[4])
    returns = ((close_price - open_price) / open_price) * 100
    save_to_cache(cache_key, returns)
    return returns


@app.get("/moneyflowclassique")
def get_moneyflowclassique(symbol, loadcash:bool, current_user: User = Depends(get_access_moneyflowclassique)):
    cache_key = f"moneyflowC_{symbol}"
    if loadcash:
        return load_from_cache(cache_key)
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
    save_to_cache(cache_key, money_flow_classique)
    return money_flow_classique


@app.get("/rsi")
def get_rsi(symbol,loadcash:bool, current_user: User = Depends(get_access_rsi)):
    cache_key = f"rsi_{symbol}"
    if loadcash:
        return load_from_cache(cache_key)
    trades = get_binance_trade_volume(symbol=symbol)
    if trades is None or len(trades) < 15:
        return None
    rsi_value = calculate_rsi(trades)
    save_to_cache(cache_key, rsi_value)
    return rsi_value


@app.get("/macd")
def get_macd(symbol,loadcash:bool, current_user: User = Depends(get_access_macd)):
    cache_key = f"macd_{symbol}"
    if loadcash:
        return load_from_cache(cache_key)
    trades = get_binance_trade_volume(symbol=symbol)
    if trades is None or len(trades) < 26:
        return None
    macd_value, signal_value = calculate_macd(trades)
    save_to_cache(cache_key, macd_value)
    return macd_value
@app.get("/sma")
def SMA(symbol,loadcash:bool, current_user: User = Depends(get_access_sma)):
    cache_key = f"sma_{symbol}"
    if loadcash:
        return load_from_cache(cache_key)
    trades = get_binance_candlestick_data(symbol=symbol)
    if trades is None:
        return None

    close_prices = [float(kline[4]) for kline in trades]

    if len(close_prices) < 10:
        return None
    sma = sum(close_prices[-10:]) / 10
    save_to_cache(cache_key, sma)
    return sma

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user.username, "token_type": "bearer"}

@app.get("/profil")
def users_profil(current_user: User = Depends(get_current_user)):
    return current_user


@app.put("/updateSubscription")
def update_subscription(SubscriptionUpdate, current_user: User = Depends(get_current_user)):
    return update_user_subscription(current_user, SubscriptionUpdate)


@app.post("/register")
def register(
    username: str = Form(...),
    password: str = Form(...),
    full_name: str = Form(...),
    email: str = Form(...),
    abonement: str = Form(...),
):
    return save_new_user(username, password, full_name, email, abonement)

@app.delete("/delete_user")
def delete_my_account(username: str = Form(...), current_user: User = Depends(get_current_user)):
    return delete_user(username, current_user)




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
