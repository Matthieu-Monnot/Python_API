import requests

"""
response = requests.get("https://api.publicapis.org/entries")
data = response.json()

# Imprimer les premiers 10 entrées
for entry in data['entries'][:10]:
    print(entry['API'], "-", entry['Description'])

response = requests.get("https://api.publicapis.org/entries?category=finance")
finance_data = response.json()
for entry in finance_data['entries']:
    print(entry['API'], "-", entry['Description'])


url = "https://api.coingecko.com/api/v3/coins/list"
response = requests.get(url)
coins = response.json()
# Imprimer les premiers 10 noms de cryptomonnaies et leurs identifiants
for coin in coins[:10]:
    print(coin['id'], "-", coin['name'])
   

coin_id = "bitcoin" # Remplacez ceci par un autre identifiant si vous le souhaitez
detailed_url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
detailed_response = requests.get(detailed_url)
coin_details = detailed_response.json()
# Imprimer des informations clés
print(coin_details['name'])
print("Valeur actuelle:", coin_details['market_data']['current_price']['usd'], "USD")

"""


def get_24h_volume(coin_id, currencies):
    volumes = [0]*len(currencies)
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/tickers?order=volume_desc"
    response = requests.get(url)
    ls_vol = response.json()["tickers"]
    for elem in ls_vol:
        if elem["target"] in currencies:
            volumes[currencies.index(elem["target"])] += round(elem["volume"])
    return dict(zip(currencies, volumes))


if __name__ == "__main__":
    currencies = ["USD", "EUR", "USDT", "USDC"]
    coins = ["bitcoin", "ethereum"]
    for coin in coins:
        print("Le volume journalier de", coin, "est :", get_24h_volume(coin_id=coin, currencies=currencies))

"""
OUTPUT:

Le volume journalier de bitcoin est : {'USD': 33599, 'EUR': 2652, 'USDT': 281595, 'USDC': 36194}
Le volume journalier de ethereum est : {'USD': 338391, 'EUR': 14773, 'USDT': 3515600, 'USDC': 2589777}
"""