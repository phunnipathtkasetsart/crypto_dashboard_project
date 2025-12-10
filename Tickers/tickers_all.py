from crypto_ticker import CryptoTicker

class XRPTicker(CryptoTicker):
    def __init__(self, parent):
        super().__init__(parent, "xrpusdt", "XRP/USDT")

class SOLTicker(CryptoTicker):
    def __init__(self, parent):
        super().__init__(parent, "solusdt", "SOL/USDT")
        
class SHIBTicker(CryptoTicker):
     def __init__(self, parent):
      super().__init__(parent, 'shibusdt', 'SHIB/USDT')

class MATICTicker(CryptoTicker):
     def __init__(self, parent):
      super().__init__(parent, 'maticusdt', 'MATIC/USDT')

class LTCTicker(CryptoTicker):
     def __init__(self, parent):
      super().__init__(parent, 'ltcusdt', 'LTC/USDT')

class LINKTicker(CryptoTicker):
     def __init__(self, parent):
      super().__init__(parent, 'linkusdt', 'LINK/USDT')

class ETHTicker(CryptoTicker):
    def __init__(self, parent):
        super().__init__(parent, "ethusdt", "ETH/USDT")

class DOTTicker(CryptoTicker):
     def __init__(self, parent):
        super().__init__(parent, 'dotusdt', 'DOT/USDT')

class DOGETicker(CryptoTicker):
     def __init__(self, parent):
        super().__init__(parent, 'dogeusdt', 'DOGE/USDT')

class BTCTicker(CryptoTicker):
    def __init__(self, parent):
        super().__init__(parent, "btcusdt", "BTC/USDT")

class BNBTicker(CryptoTicker):
    def __init__(self, parent):
        super().__init__(parent, "bnbusdt", "BNB/USDT")

class ADATicker(CryptoTicker):
    def __init__(self, parent):
        super().__init__(parent, "adausdt", "ADA/USDT")

