from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta
from client import Client


class Chart:
    def __init__(self, uuid=0, instrument=None, time_frame=1, height=15, width=60, start_date=datetime.now()-timedelta(weeks=1), end_date=datetime.now()-timedelta(hours=5)):
        self.data=None
        self.client=Client()
        self.uuid = uuid
        self.instrument = instrument
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
        elif self.time_frame>=60*24*3.5:
            data_time_frame=TimeFrame.Week
        elif self.time_frame>=60*24*7*15:
            data_time_frame=TimeFrame.Month
      
        self.data = self.client.get_data(self.uuid, self.start_date, self.end_date, data_time_frame)

    def update(self, uuid=False, instrument=False, time_frame=False, height=False, width=False, start_date=False, end_date=False):
        if uuid: self.uuid = uuid
        if instrument: self.instrument = instrument
        if time_frame: self.time_frame = time_frame
        if height: self.height = height
        if width: self.width = width
        if start_date: self.start_date
        if end_date: self.end_date

    def get_params(self):
        return dict(uuid=self.uuid,instrument=self.instrument,time_frame=self.time_frame,height=self.height,width=self.width)
  
    def get_data(self):
        return self.data
  