# test_binance_api.py
import requests

def test_rest_api(symbols=[
                        "BTCUSDT" ,
                        "ETHUSDT",
                        "BNBUSDT",
                        "SOLUSDT",
                        "ADAUSDT",
                        "XRPUSDT",
                        "DOGEUSDT",
                        "DOTUSDT",
                        "LINKUSDT",
                        "LTCUSDT",
                        "SHIBUSDT"]):
    
    """Test basic REST API connectivity."""
    url = "https://api.binance.com/api/v3/ticker/price"
    for symbol in symbols:
        try:
            response = requests.get(url, params={"symbol": symbol}, timeout=5)
            response.raise_for_status()
            data = response.json()
            print(f"✓ REST API works: {symbol} = ${data['price']}")
        except Exception as e:
            print(f"✗ REST API failed: {e}")
            return False
    return True

def test_websocket():
    """Test basic WebSocket connectivity."""
    import websocket
    import json
    import threading

    symbols = [
        "BTCUSDT" ,
        "ETHUSDT",
        "BNBUSDT",
        "SOLUSDT",
        "ADAUSDT",
        "XRPUSDT",
        "DOGEUSDT",
        "DOTUSDT",
        "LINKUSDT",
        "LTCUSDT",
        "SHIBUSDT"
    ]
    received_data = False

    stream = "/".join([f"{s.lower()}@ticker" for s in symbols])
    url = f"wss://stream.binance.com:9443/stream?streams={stream}"

    def on_message(ws, message):
        nonlocal received_data
        data_json = json.loads(message)
        data = data_json['data']
        symbol = data['s']
        price = data['c']
        print(f"✓ WebSocket works: {symbol} = ${price}")
        received_data = True

    def on_error(ws, error):
        print(f"✗ WebSocket failed: {error}")

    ws = websocket.WebSocketApp(
        url,
        on_message=on_message,
        on_error=on_error
    )

    thread = threading.Thread(target=ws.run_forever)
    thread.daemon = True
    thread.start()
    thread.join(timeout=5)

    return received_data


if __name__ == "__main__":
    print("Testing Binance API connectivity...\n")
    rest_ok = test_rest_api()
    ws_ok = test_websocket()
    
    if rest_ok and ws_ok:
        print("\n✓ All tests passed! Ready to build dashboard.")
    else:
        print("\n✗ Some tests failed. Check your internet connection.")
