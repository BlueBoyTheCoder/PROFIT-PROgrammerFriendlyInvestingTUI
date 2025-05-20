from PASSWORD import API_KEY, SECRET_KEY
from exceptions import *
from alpaca.data.historical import CryptoHistoricalDataClient, StockHistoricalDataClient, OptionHistoricalDataClient
from alpaca.trading.client import TradingClient
from alpaca.data.requests import CryptoBarsRequest, StockBarsRequest, OptionBarsRequest
from alpaca.trading.models import Asset
from alpaca.trading.enums import AssetClass
from alpaca.data.enums import DataFeed
from alpaca.data.timeframe import TimeFrame
import yfinance as yf #Necessary for newest data. Alpaca doesn't support newest data
from datetime import datetime, timedelta, timezone
from alpaca.common.exceptions import APIError



class Client:
    def __init__(self, api_key=None, secret_key=None, paper=True):
        if api_key and secret_key:
            self.client = TradingClient(api_key,secret_key, paper=paper)
            self.crypto_client = CryptoHistoricalDataClient(api_key,secret_key)
            self.stock_client = StockHistoricalDataClient(api_key,secret_key)
            self.option_client = OptionHistoricalDataClient(api_key,secret_key)
        elif not api_key and not secret_key:
            self.client = TradingClient(API_KEY,SECRET_KEY, paper=paper)
            self.crypto_client = CryptoHistoricalDataClient(API_KEY,SECRET_KEY)
            self.stock_client = StockHistoricalDataClient(API_KEY,SECRET_KEY)
            self.option_client = OptionHistoricalDataClient(API_KEY,SECRET_KEY)
        else:
            raise InvalidKey("Your API_KEY or SECRET_KEY is invalid or undetermined")
        

    def get_trading_client(self):
        return self.client


    def get_client_status(self):
        return dict(filter(lambda item: item[0] in ['status','crypto_status','options_buying_power'],dict(self.client.get_account()).items()))
   
    
    def get_client_positions(self):
        return [dict(filter(lambda item: item[0] in ['symbol','qty','avg_entry_price','current_price'],dict(position).items())) for position in self.client.get_all_positions()]


    def get_client_orders(self):
        return [dict(filter(lambda item: item[0] in ['symbol','qty','side','type','time_in_force','avg_entry_price','current_price','created_at','expired_at','filled_at'],dict(position).items())) for position in self.client.get_orders()]

    


    def get_historical_data(self, uuid: Asset, start_time, end_time, data_time_frame: TimeFrame):
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
                                symbol_or_symbols=uuid,
                                timeframe=data_time_frame,
                                start=start_time,
                                end=end_time
                            )

        bars = get_bars(local_request_params)

        return [dict(filter(lambda item: item[0] in ['timestamp', 'open', 'close', 'low', 'high'],dict(b).items())) for b in bars[uuid]] 
    

    def get_lastday_data(self, uuid: Asset | str):
        right_formats={
            ('datetime',''): 'timestamp',
            ('Open',uuid): 'open',
            ('High',uuid): 'high',
            ('Low',uuid): 'low',
            ('Close',uuid): 'close'
        }

        data = yf.download(uuid, period="1d", interval="5m", progress=False, auto_adjust=True)

        data = data.reset_index()

        data = data.rename(columns={"Datetime": "datetime"})
        data = data.to_dict(orient="records")

        for d in data:
            d[('datetime','')] = d[('datetime','')].to_pydatetime()

        for d in data:
            for right_format in right_formats:
                if right_format in d:
                    d[right_formats[right_format]]=d.pop(right_format)
            if ('Volume',uuid) in d:
                d.pop(('Volume',uuid))

        return data
            

    def get_newest_data(self, uuid: Asset | str, start_time, end_time, data_time_frame):
        right_formats={
            ('datetime',''): 'timestamp',
            ('Open',uuid): 'open',
            ('High',uuid): 'high',
            ('Low',uuid): 'low',
            ('Close',uuid): 'close'
        }

        match(data_time_frame.unit):
            case TimeFrame.Minute.unit:
                interval="5m"
            case TimeFrame.Hour.unit:
                interval="1h"
            case TimeFrame.Day.unit:
                interval="1d"


        data = yf.download(uuid, start=start_time.strftime('%Y-%m-%d'), end=end_time.strftime('%Y-%m-%d'),interval=interval, progress=False, auto_adjust=True)
        data = data.reset_index()
        data = data.rename(columns={"Datetime": "datetime", "Date": "datetime"})
        data = data.to_dict(orient="records")
        
        
        for d in data:
            d[('datetime','')] = d[('datetime','')].to_pydatetime()

        for d in data:
            for right_format in right_formats:
                if right_format in d:
                    d[right_formats[right_format]]=d.pop(right_format)
            if ('Volume',uuid) in d:
                d.pop(('Volume',uuid))

        return data


    def get_data(self, uuid: Asset, start_time, end_time, data_time_frame: TimeFrame):
        utc_m4 = timezone(timedelta(hours=-4))
        date_3d_back = datetime.now(utc_m4)-timedelta(days=7)
        if start_time < date_3d_back and end_time > date_3d_back:
            return self.get_historical_data(uuid, start_time, date_3d_back, data_time_frame) + self.get_newest_data(uuid,date_3d_back,end_time,data_time_frame)
        elif start_time > date_3d_back and end_time > date_3d_back:
            return self.get_newest_data(uuid,start_time,end_time,data_time_frame)
        else:
            return self.get_historical_data(uuid, start_time, end_time, data_time_frame)


    def uuid_exists(self, uuid: str):
        try:
            self.client.get_asset(uuid)
        except APIError:
            return False
        return True