from crypto_ticker import CryptoTicker

class LINKTicker(CryptoTicker):
     def __init__(self, parent):
      super().__init__(parent, 'linkusdt', 'LINK/USDT')