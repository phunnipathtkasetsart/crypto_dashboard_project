from crypto_ticker import CryptoTicker

class ADATicker(CryptoTicker):
    def __init__(self, parent):
        super().__init__(parent, "adausdt", "ADA/USDT")
