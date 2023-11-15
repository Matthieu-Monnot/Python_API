import websocket
import json

socket = 'wss://stream.binance.com/ws'


def on_open(ws):
    subscribe_message = {"method": "SUBSCRIBE",
                         "params": ["btcusdt@depth@100ms"],
                         "id": 1}
    ws.send(json.dumps(subscribe_message))


def on_message(ws, message):
    print("received a message")
    print(json.loads(message))


def on_close(ws):
    print("closed connection")


if __name__ == "__main__":
    ws = websocket.WebSocketApp(socket + '/btcusdt@depth@100ms', on_open=on_open, on_message=on_message, on_close=on_close)
    ws.run_forever()

trade = {'e': 'trade', 'E': 1700000462100, 's': 'BTCUSDT', 't': 3280966314, 'p': '35528.03000000', 'q': '0.00108000', 'b': 23249358445, 'a': 23249358743, 'T': 1700000462099, 'm': True, 'M': True}
bidask = {'e': 'depthUpdate', 'E': 1700081539342, 's': 'BTCUSDT', 'U': 40391409386, 'u': 40391409398, 'b': [['37451.10000000', '1.89754000'], ['37290.01000000', '0.00000000'], ['33705.00000000', '0.03756000']], 'a': [['37451.11000000', '1.84060000'], ['37461.98000000', '1.60256000'], ['37475.92000000', '0.00000000'], ['37499.01000000', '0.03943000'], ['37599.99000000', '0.00175000'], ['37751.11000000', '0.00100000']]}

