from crypto_ticker import CryptoTicker

class DOGETicker(CryptoTicker):
     def __init__(self, parent):
        super().__init__(parent, 'dogeusdt', 'DOGE/USDT')