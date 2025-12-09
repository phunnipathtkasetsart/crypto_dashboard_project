from crypto_ticker import CryptoTicker

class BNBTicker(CryptoTicker):
    def __init__(self, parent):
        super().__init__(parent, "bnbusdt", "BNB/USDT")
