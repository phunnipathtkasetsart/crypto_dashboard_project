from crypto_ticker import CryptoTicker

class XRPTicker(CryptoTicker):
    def __init__(self, parent):
        super().__init__(parent, "xrpusdt", "XRP/USDT")
