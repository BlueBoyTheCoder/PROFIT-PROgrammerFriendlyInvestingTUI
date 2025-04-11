from PASSWORD import API_KEY, SECRET_KEY
from exceptions import *
from alpaca.data.historical import CryptoHistoricalDataClient, StockHistoricalDataClient, OptionHistoricalDataClient
from alpaca.data.requests import StockLatestTradeRequest, OptionLatestTradeRequest, CryptoLatestTradeRequest, StockLatestQuoteRequest, OptionLatestQuoteRequest, CryptoLatestQuoteRequest
#from alpaca.data.live import CryptoDataStream, StockDataStream, OptionDataStream
from alpaca.trading.client import TradingClient
from alpaca.data.requests import CryptoBarsRequest, StockBarsRequest, OptionBarsRequest
from alpaca.trading.models import Asset
from alpaca.trading.enums import AssetClass
#from alpaca.data.enums import DataFeed



class Client:
    def __init__(self, api_key=None, secret_key=None):
        if api_key and secret_key:
            self.client = TradingClient(api_key,secret_key)
            self.crypto_client=CryptoHistoricalDataClient(api_key,secret_key)
            self.stock_client=StockHistoricalDataClient(api_key,secret_key)
            self.option_client=OptionHistoricalDataClient(api_key,secret_key)
        elif not api_key and not secret_key:
            self.client = TradingClient(API_KEY,SECRET_KEY)
            self.crypto_client=CryptoHistoricalDataClient(API_KEY,SECRET_KEY)
            self.stock_client=StockHistoricalDataClient(API_KEY,SECRET_KEY)
            self.option_client=OptionHistoricalDataClient(API_KEY,SECRET_KEY)
        else:
            raise InvalidKey("Your API_KEY or SECRET_KEY is invalid or undetermined")
        

    def get_client_status(self):
        return dict(filter(lambda item: item[0] in ['status','crypto_status','options_buying_power'],dict(self.client.get_account()).items()))
   
    
    def get_client_positions(self):
        return [dict(filter(lambda item: item[0] in ['symbol','qty','avg_entry_price','current_price'],dict(position).items())) for position in self.client.get_all_positions()]


    def get_data(self, uuid: Asset, start_time, end_time, data_time_frame):
        if self.client.get_asset(uuid).asset_class == AssetClass.CRYPTO:
            get_bars = self.crypto_client.get_crypto_bars
            local_request = CryptoBarsRequest
        elif self.client.get_asset(uuid).asset_class == AssetClass.US_EQUITY:
            get_bars = self.stock_client.get_stock_bars
            local_request = StockBarsRequest
        elif self.client.get_asset(uuid).asset_class == AssetClass.US_OPTION:
            get_bars = self.option_client.get_option_bars
            local_request = OptionBarsRequest
        else:
            raise InvalidAssetClass()

        local_request_params = local_request(
                                symbol_or_symbols = uuid,
                                timeframe = data_time_frame,
                                start = start_time,
                                end = end_time
                            )

        bars = get_bars(local_request_params)

        return [dict(filter(lambda item: item[0] in ['timestamp', 'open', 'close', 'low', 'high'],dict(b).items())) for b in bars[uuid]]
    
    
    def get_newest_data(self, uuid: Asset):
        if self.client.get_asset(uuid).asset_class == AssetClass.CRYPTO:
            get_news = self.crypto_client.get_crypto_latest_trade
            local_request = CryptoLatestTradeRequest
        elif self.client.get_asset(uuid).asset_class == AssetClass.US_EQUITY:
            get_news = self.stock_client.get_stock_latest_trade
            local_request = OptionLatestTradeRequest
        elif self.client.get_asset(uuid).asset_class == AssetClass.US_OPTION:
            get_news = self.option_client.get_option_latest_trade
            local_request = StockLatestTradeRequest
        else:
            raise InvalidAssetClass()

        local_request_params = local_request(symbol_or_symbols = uuid)

        latest_trade = get_news(local_request_params)

        return dict(filter(lambda item: item[0] in ['timestamp', 'price'],dict(latest_trade[uuid]).items())) 
    