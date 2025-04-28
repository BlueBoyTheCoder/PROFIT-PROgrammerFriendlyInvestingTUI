from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta, timezone
from client import Client



class Widget:
    def __init__(self, instruments_uuid=None):
        self.client = Client()
        if instruments_uuid: 
            if type(instruments_uuid)==str: self.instruments=dict([(instruments_uuid,None)])
            elif type(instruments_uuid)==list: self.instruments=dict([(inst,None) for inst in instruments_uuid])
        else: self.instruments = dict()


    def add_instrument(self,instruments_uuid: str | list):
        if type(instruments_uuid)==str: self.instruments[instruments_uuid]=None
        elif type(instruments_uuid)==list:
            for inst in instruments_uuid: self.instruments[inst]=None

    
    def pop_instrument(self,instruments_uuid: str | list):
        if type(instruments_uuid)==str: 
            self.instruments.pop(instruments_uuid)
        elif type(instruments_uuid)==list: 
            for inst in instruments_uuid: self.instruments.pop(inst)


    def reload_instruments(self):
        for uuid in self.instruments:
            data = self.client.get_newest_data(uuid)[0]
            data_dict=dict()
            data_dict['timestamp']=data['timestamp']
            data_dict['price']=round(data['close'],2)
            data_dict['change']=round(100*(data['close']/data['open']-1),2)

            self.instruments[uuid]=data_dict   
    

    def reload_instrument(self, uuid):
        data = self.client.get_newest_data(uuid)[0]
        data_dict=dict()
        data_dict['timestamp']=data['timestamp']
        data_dict['price']=round(data['close'],2)
        data_dict['change']=round(100*(data['close']/data['open']-1),2)

        self.instruments[uuid]=data_dict    

    
    def get_instruments_data(self):
        return self.instruments
    

    def get_widget_patch(self, max_length):
        self.reload_instruments()
        whole_patch=[]
        length=0
        for uuid in self.instruments:
            uuid_data=self.get_instruments_data()[uuid]
            string=uuid+" "+str(uuid_data['price'])+" "+str(uuid_data['change'])+"%"
            if uuid_data['change']>0:
                patch=(string,1)
                length+=len(string)+6
            elif uuid_data['change']<0:
                patch=(string,-1)
                length+=len(string)+6
            else:
                patch=(string,0)
                length+=len(string)+5
            
            if length>max_length:
                return whole_patch
            
            whole_patch.append(patch)
        
        return whole_patch

  
