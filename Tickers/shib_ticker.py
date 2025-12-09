from crypto_ticker import CryptoTicker

class SHIBTicker(CryptoTicker):
     def __init__(self, parent):
      super().__init__(parent, 'shibusdt', 'SHIB/USDT')