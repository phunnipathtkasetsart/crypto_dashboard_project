from crypto_ticker import CryptoTicker

class DOTTicker(CryptoTicker):
     def __init__(self, parent):
        super().__init__(parent, 'dotusdt', 'DOT/USDT')