from crypto_ticker import CryptoTicker

class ETHTicker(CryptoTicker):
    def __init__(self, parent):
        super().__init__(parent, "ethusdt", "ETH/USDT")