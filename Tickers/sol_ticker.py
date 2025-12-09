from crypto_ticker import CryptoTicker

class SOLTicker(CryptoTicker):
    def __init__(self, parent):
        super().__init__(parent, "solusdt", "SOL/USDT")
