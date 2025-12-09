a = ['doge','dot','link','matic','ltc','shib']
for i in a:
    with open(f'{i}_ticker.py' , 'w')as file:
        file.write(f"from crypto_ticker import CryptoTicker\n\nclass {i.upper()}Ticker(CryptoTicker):\n     def __init__(self, parent):\n   super().__init__(parent, '{i.lower()}usdt', '{i.upper()}/USDT')")