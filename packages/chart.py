from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta
from client import Client


class Chart:
    def __init__(self, uuid=0, time_frame=30, height=15, width=60, start_date=datetime.now() - timedelta(weeks=1), end_date=datetime.now() - timedelta(hours=5)):
        self.data = None
        self.client = Client()
        self.uuid = uuid
        self.time_frame = time_frame  # minutes (time per one char. Ex: time_frame=3 and width=15 then timespan=3*15=45 minutes on 15 char of width)
        self.height = height
        self.width = width
        self.start_date = start_date
        self.end_date = end_date

    def reload(self):
        """        
        Choose right accuracy of chart 
        Gets current data
        """        
        data_time_frame = TimeFrame.Minute
        if self.time_frame >= 60:
            data_time_frame = TimeFrame.Hour
        if self.time_frame >= 1920:
            data_time_frame = TimeFrame.Day

        self.data = self.client.get_data(self.uuid, self.start_date, self.end_date, data_time_frame)

    def get_current_price(self):
        """
        Gets current price
        """
        return self.client.get_lastday_data(self.uuid)[0]["close"]

    def update(self, uuid=False, time_frame=False, height=False, width=False, start_date=False, end_date=False):
        """
        Update parameters that has non negative evaluation
        """
        if uuid:
            self.uuid = uuid
        if time_frame:
            self.time_frame = time_frame
        if height:
            self.height = height
        if width:
            self.width = width
        if start_date:
            self.start_date = start_date
        if end_date:
            self.end_date = end_date

    def get_params(self):
        """
        Return parameters od chart in dictionary
        """
        return dict(uuid=self.uuid, time_frame=self.time_frame, height=self.height, width=self.width)

    def get_data(self):
        return self.data

    def get_newest_data(self):
        """
        Returns newest data for chart
        """
        return self.client.get_newest_data(self.uuid)
