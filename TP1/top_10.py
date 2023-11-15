import requests
import pandas as pd
from main import get_24h_volume


def get_more_liquid_asset(n):
    # On prend les 10 cryptos les plus liquides contre l'usd
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd"
    response = requests.get(url)
    coin_details = response.json()
    df = pd.DataFrame()
    for i in range(len(coin_details)):
        if coin_details[i]["id"] not in ["bitcoin", "ethereum"]:
            df = pd.concat([df, pd.DataFrame([coin_details[i]])], ignore_index=True)
    df.sort_values(by=["total_volume"])
    return df.head(n)


if __name__ == "__main__":
    currencies = ["USD", "EUR", "USDT", "USDC"]
    df_top_10 = get_more_liquid_asset(n=10)
    print(df_top_10)
    for j in range(len(df_top_10)):
        print("Le volume journalier de", df_top_10.loc[j, "id"], "est :", get_24h_volume(coin_id=df_top_10.loc[j, "id"], currencies=currencies))

"""
OUTPUT : 
                 id  ...              last_updated
0            tether  ...  2023-11-07T19:55:00.334Z
1       binancecoin  ...  2023-11-07T19:58:56.557Z
2            ripple  ...  2023-11-07T19:58:53.922Z
3          usd-coin  ...  2023-11-07T19:58:57.744Z
4            solana  ...  2023-11-07T19:58:51.600Z
5      staked-ether  ...  2023-11-07T19:58:35.758Z
6           cardano  ...  2023-11-07T19:58:55.306Z
7          dogecoin  ...  2023-11-07T19:58:58.834Z
8  the-open-network  ...  2023-11-07T19:58:50.898Z
9              tron  ...  2023-11-07T19:58:57.462Z

[10 rows x 26 columns]
Le volume journalier de tether est : {'USD': 355232591, 'EUR': 201312610, 'USDT': 30642032885, 'USDC': 0}
Le volume journalier de binancecoin est : {'USD': 33691, 'EUR': 10086, 'USDT': 2809446, 'USDC': 20717}
Le volume journalier de ripple est : {'USD': 301766808, 'EUR': 108909962, 'USDT': 2663848157, 'USDC': 127574369}
Le volume journalier de usd-coin est : {'USD': 28159454, 'EUR': 21998827, 'USDT': 922351863, 'USDC': 214735838}
Le volume journalier de solana est : {'USD': 4951877, 'EUR': 963142, 'USDT': 30999781, 'USDC': 485170}
Le volume journalier de staked-ether est : {'USD': 0, 'EUR': 0, 'USDT': 342, 'USDC': 17}
Le volume journalier de cardano est : {'USD': 121909570, 'EUR': 51982273, 'USDT': 935174998, 'USDC': 27004601}
Le volume journalier de dogecoin est : {'USD': 876170522, 'EUR': 80017030, 'USDT': 13696055544, 'USDC': 67253795}
Le volume journalier de the-open-network est : {'USD': 234118, 'EUR': 0, 'USDT': 26102768, 'USDC': 33440}
Le volume journalier de tron est : {'USD': 14526018, 'EUR': 22322938, 'USDT': 2144608152, 'USDC': 31482704}
"""
