import requests


def get_coins(n):
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc"
    response = requests.get(url)
    ls_coins = response.json()
    return [coin["id"] for coin in ls_coins][:n]


def get_24h_volume_btc_eth(coin_id):
    volumes = [0, 0]
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/tickers?order=volume_desc"
    response = requests.get(url)
    ls_vol = response.json()["tickers"]
    for elem in ls_vol:
        if elem["target"] == "BTC":
            volumes[0] += elem["volume"] * elem["last"]
        elif elem["base"] == "BTC":
            volumes[0] += elem["volume"] / elem["last"]
        if elem["target"] == "ETH":
            volumes[1] += elem["volume"] * elem["last"]
        elif elem["base"] == "ETH":
            volumes[1] += elem["volume"] / elem["last"]
    return {"bitcoin": volumes[0], "ethereum": volumes[1]}


def get_more_liquid_asset_vs_btc_eth(n):
    # On choisit ici de calculer les cryptos les n plus liquides vs BTC et ETH sur la base des 3*n plus liquides vs usd
    # et plus importants en terme de capitalisation
    assets = get_coins(n=3*n)
    volumes = dict(zip(assets, [0]*len(assets)))
    for asset in assets:
        volumes[asset] = get_24h_volume_btc_eth(coin_id=asset)
    return sorted(volumes.items(), key=lambda x: x[1]["bitcoin"] + x[1]["ethereum"], reverse=True)[2:n+2]


if __name__ == "__main__":
    df_top_3 = get_more_liquid_asset_vs_btc_eth(n=3)
    print(df_top_3)

"""
OUTPUT :

('binancecoin', {'bitcoin': 559.579407539223, 'ethereum': 2846.2657685242198}), 
('ripple', {'bitcoin': 1267.3287728554296, 'ethereum': 1878.6143166799998}), 
('solana', {'bitcoin': 815.8167675606777, 'ethereum': 1152.8536662860001})
"""