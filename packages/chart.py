from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta, timezone
from client import Client



class Chart:
    def __init__(self, uuid=0, time_frame=30, height=15, width=60, start_date=datetime.now()-timedelta(weeks=1), end_date=datetime.now()-timedelta(hours=5)):
        self.data = None
        self.instruments = dict()
        self.client = Client()
        self.uuid = uuid
        self.time_frame = time_frame #minutes (time per one char. Ex: time_frame=3 and width=15 then timespan=3*15=45 minutes on 15 char of width)
        self.height = height
        self.width = width
        self.start_date = start_date
        self.end_date = end_date


    def reload(self):
        data_time_frame=TimeFrame.Minute
        if self.time_frame>=30:
            data_time_frame=TimeFrame.Hour
        elif self.time_frame>=60*12:
            data_time_frame=TimeFrame.Day
        elif self.time_frame>=60*24*7/2:
            data_time_frame=TimeFrame.Week
        elif self.time_frame>=60*24*7*15:
            data_time_frame=TimeFrame.Month
      
        self.data = self.client.get_historical_data(self.uuid, self.start_date, self.end_date, data_time_frame)


    def update(self, uuid=False, time_frame=False, height=False, width=False, start_date=False, end_date=False):
        if uuid: self.uuid = uuid
        if time_frame: self.time_frame = time_frame
        if height: self.height = height
        if width: self.width = width
        if start_date: self.start_date
        if end_date: self.end_date


    def get_params(self):
        return dict(uuid=self.uuid,time_frame=self.time_frame,height=self.height,width=self.width)
  

    def get_data(self):
        return self.data
    

    def get_newest_data(self):
        return self.client.get_newest_data(self.uuid)
    

    def add_instrument(self,uuid):
        self.instruments[uuid]=None

    
    def pop_instrument(self,uuid):
        self.instruments.pop(uuid)


    #To be changed with stream of data!!!
    def reload_instruments(self):
        for uuid in self.instruments:
            utc_m4 = timezone(timedelta(hours=-4))
            data = self.client.get_historical_data(uuid,datetime.now(utc_m4)-timedelta(days=2),datetime.now(utc_m4)-timedelta(days=1),TimeFrame.Day)[0]
            
            data_dict=dict()
            data_dict['timestamp']=data['timestamp']
            data_dict['price']=data['close']
            data_dict['change']=data['close']/data['open']-1

            self.instruments[uuid]=data_dict   
    

    def reload_instrument(self, uuid):
        utc_m4 = timezone(timedelta(hours=-4))
        data = self.client.get_data(uuid,datetime.now(utc_m4)-timedelta(days=2),datetime.now(utc_m4)-timedelta(days=1),TimeFrame.Day)[0]
        
        data_dict=dict()
        data_dict['timestamp']=data['timestamp']
        data_dict['price']=data['close']
        data_dict['change']=data['close']/data['open']-1

        self.instruments[uuid]=data_dict    

    
    def get_instruments_data(self):
        return self.instruments
  