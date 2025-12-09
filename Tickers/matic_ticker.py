from crypto_ticker import CryptoTicker

class MATICTicker(CryptoTicker):
     def __init__(self, parent):
      super().__init__(parent, 'maticusdt', 'MATIC/USDT')