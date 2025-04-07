from PASSWORD import API_KEY, SECRET_KEY
from alpaca.data.historical import CryptoHistoricalDataClient, StockHistoricalDataClient, OptionHistoricalDataClient
from alpaca.trading.client import TradingClient
from alpaca.data.requests import CryptoBarsRequest, StockBarsRequest, OptionBarsRequest
from alpaca.trading.models import Asset
from alpaca.trading.enums import AssetClass


class Client:
    def __init__(self):
        self.client = TradingClient(API_KEY,SECRET_KEY)

    def get_data(self, uuid: Asset, start_time, end_time, data_time_frame):
        if self.client.get_asset(uuid).asset_class == AssetClass.CRYPTO:
            get_bars = CryptoHistoricalDataClient(API_KEY,SECRET_KEY).get_crypto_bars
            local_request = CryptoBarsRequest
        elif self.client.get_asset(uuid).asset_class == AssetClass.US_EQUITY:
            get_bars = StockHistoricalDataClient(API_KEY,SECRET_KEY).get_stock_bars
            local_request = StockBarsRequest
        elif self.client.get_asset(uuid).asset_class == AssetClass.US_OPTION:
            get_bars = OptionHistoricalDataClient(API_KEY,SECRET_KEY).get_option_bars
            local_request = OptionBarsRequest
        else:
            raise Exception("No AssetClass match")

        local_request_params = local_request(
                                symbol_or_symbols = uuid,
                                timeframe = data_time_frame,
                                start = start_time,
                                end = end_time
                            )

        bars = get_bars(local_request_params)

        return [dict(filter(lambda item: item[0] in ['timestamp', 'open', 'close', 'low', 'high'],dict(b).items())) for b in bars[uuid]]
