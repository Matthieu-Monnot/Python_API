import requests


url = "https://api.coingecko.com/api/v3/coins/list"
response = requests.get(url)
js_res = response.json()
convert_symbol_id = dict(zip([elem["id"] for elem in js_res], [elem["symbol"] for elem in js_res]))


def get_stablecoins(n):
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&category=stablecoins&order=market_cap_desc"
    response = requests.get(url)
    return response.json()[:n]


def get_24h_volume_stable(stablecoins):
    total_volumes = dict(zip(stablecoins, [0]*len(stablecoins)))
    for stablecoin in stablecoins:
        url = f"https://api.coingecko.com/api/v3/coins/{stablecoin}/tickers?order=volume_desc"
        response = requests.get(url)
        ls_vol = response.json()["tickers"]
        for elem in ls_vol:
            if elem["target"].lower() == convert_symbol_id[stablecoin]:
                total_volumes[stablecoin] += elem["volume"] * elem["last"]
            elif elem["base"].lower() == convert_symbol_id[stablecoin]:
                total_volumes[stablecoin] += elem["volume"] / elem["last"]
    return sorted(total_volumes.items(), key=lambda x: x[1], reverse=True)[:3]


if __name__ == "__main__":
    stablecoins = [stablecoin["id"] for stablecoin in get_stablecoins(n=10)]
    print(stablecoins)
    print(get_24h_volume_stable(stablecoins=stablecoins))

"""
OUTPUT:

('tether', 18341446436.711437),
('usd-coin', 5134689030.38595),
('dai', 4084417504.8347387)
"""
