from crypto_ticker import CryptoTicker

class BTCTicker(CryptoTicker):
    def __init__(self, parent):
        super().__init__(parent, "btcusdt", "BTC/USDT")