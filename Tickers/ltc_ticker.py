from crypto_ticker import CryptoTicker

class LTCTicker(CryptoTicker):
     def __init__(self, parent):
      super().__init__(parent, 'ltcusdt', 'LTC/USDT')