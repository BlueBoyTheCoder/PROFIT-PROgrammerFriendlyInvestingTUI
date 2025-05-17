from chart import *
from datetime import datetime, timedelta, timezone, date
import curses
import time


class ChartDisplay(Chart):
    def __init__(self, uuid=0, time_frame=30, height=15, width=60, start_date=None, end_date=None, start_price=100, end_price=300):
        self.chart=None
        self.chart_available=True
        self.place_for_data=4
        self.place_for_price=7
        self.start_price=start_price
        self.end_price=end_price
        ###bez if ustalić wcześńiej
        # if start_date is None:
        #     super().__init__(uuid, time_frame, height, width, datetime.now()-timedelta(minutes=time_frame*(width-self.place_for_price)), datetime.now())
        # else:
        super().__init__(uuid, time_frame, height, width, start_date, end_date)
        

    def update(self, uuid=False, time_frame=False, height=False, width=False, start_date=False, end_date=False):
        # super().update(uuid, time_frame, height, width, start_date, end_date)
        # self.start_date=start_date

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
        


    
    def create_chart(self):
        chart=[dict() for _ in range(self.width-self.place_for_price)]
        
        self.reload()
        price=[]

        for d in self.data:
            if self.time_frame>=1920:
                price.append((d['open'],d['close'],d['timestamp'].replace(hour=0),1))
            else:
                price.append((d['open'],d['close'],d['timestamp'],1))
            


        price_max=self.end_price
        price_min=self.start_price
        price_delta=price_max-price_min

        price_step=price_delta/(self.height-self.place_for_data)

        date=price[0][2]
        date=self.start_date
        date=date.replace(tzinfo=timezone.utc)

        subparts=0


        # enum
        match self.time_frame:
            case 15:
                subparts=15
                time_step=timedelta(minutes=1)
                date=date.replace(second=0, microsecond=0)
            case 30:
                subparts=30
                time_step=timedelta(minutes=1)
                date=date.replace(second=0, microsecond=0)
            case 60:
                subparts=1
                time_step=timedelta(hours=1)
                date=date.replace(minute=0, second=0, microsecond=0)
            case 120:
                subparts=2
                time_step=timedelta(hours=1)
                date=date.replace(minute=0, second=0, microsecond=0)
            case 240:
                subparts=4
                time_step=timedelta(hours=1)
                date=date.replace(minute=0, second=0, microsecond=0)
            case 480:
                subparts=8
                time_step=timedelta(hours=1)
                date=date.replace(minute=0, second=0, microsecond=0)
            case 960:
                subparts=16
                time_step=timedelta(hours=1)
                date=date.replace(minute=0, second=0, microsecond=0)
            case 1920:
                subparts=1
                time_step=timedelta(days=1)
                date=date.replace(hour=0, minute=0, second=0, microsecond=0)
            case 3840:
                subparts=2
                time_step=timedelta(days=1)
                date=date.replace(hour=0, minute=0, second=0, microsecond=0)
            case 7680:
                subparts=4
                time_step=timedelta(days=1)
                date=date.replace(hour=0, minute=0, second=0, microsecond=0)
            case 15360:
                subparts=8
                time_step=timedelta(days=1)
                date=date.replace(hour=0, minute=0, second=0, microsecond=0)
            case 30720:
                subparts=16
                time_step=timedelta(days=1)
                date=date.replace(hour=0, minute=0, second=0, microsecond=0)
            case 61440:
                subparts=32
                time_step=timedelta(days=1)
                date=date.replace(hour=0, minute=0, second=0, microsecond=0)
            case _:
                return
            

        i_=0
        price_start,price_end=0,0
        for i in range(0, (self.width-self.place_for_price)*subparts, subparts):
            start=float("inf")
            end=-float("inf")
            for k in range(i,i+subparts):
                if k-i_>=len(price):
                    break

                if price[k-i_][2] == date + k*time_step:
                    

                    p=price[k-i_]
                    if start==float("inf"):
                        price_start=p[0]
                        start = int((p[0]-price_min)/price_step)
                    price_end=p[1]
                    end = int((p[1]-price_min)/price_step)

                else:
                    i_+=1
            
            if start!=float("inf"):
                chart[i//subparts]["start"]=min(start,end)
                chart[i//subparts]["length"]=max(1,abs(end-start))
                if price_start<price_end:
                    chart[i//subparts]["direction"]=1
                else:
                    chart[i//subparts]["direction"]=-1
            else:

                chart[i//subparts]["start"]=0
                chart[i//subparts]["length"]=0
                chart[i//subparts]["direction"]=1
                
            chart[i//subparts]["date"]=date+i*time_step    

        self.chart_available=False
        self.chart=chart
        self.chart_available=True     
    

    def print_chart(self):
        if self.chart==None or self.chart_available==False:
            print("NO CHART")
        else:
            for ch in self.chart:
                print(ch)
    

    def display_chart(self, stdscr, y, x):
        if self.chart==None or self.chart_available == False:
            return -1
        else:
            for i, ch in enumerate(self.chart):
                if ch["direction"]==1:
                    color=1
                else:
                    color=2
                for j in range(ch["start"],ch["start"]+ch["length"]):
                    if j>=0 and self.height-j-self.place_for_data>=0:
                        stdscr.attron(curses.color_pair(color))
                        stdscr.addstr(y+self.height-j-self.place_for_data, x+i, "#")
                        stdscr.attroff(curses.color_pair(color))
        
                if i%20==0:
                    stdscr.addstr(y+self.height-self.place_for_data+1, x+i, "|") 
                    stdscr.addstr(y+self.height-self.place_for_data+2, x+i, str(ch["date"].time()))
                    stdscr.addstr(y+self.height-self.place_for_data+3, x+i, str(ch["date"].date())) 
            
            for i in range(self.height-self.place_for_data):
                delta_price=(self.end_price-self.start_price)/(self.height-self.place_for_data)
                if i%10==0:
                    stdscr.addstr(y+self.height-i-self.place_for_data, x+self.width-self.place_for_price, "-") 
                    stdscr.addstr(y+self.height-i-self.place_for_data, x+self.width-self.place_for_price+2, str(round(self.start_price+delta_price*i,1))) 
        stdscr.refresh()


    def price_up(self, factor=0.25):
        delta_price=self.end_price-self.start_price
        self.start_price+=delta_price*factor
        self.end_price+=delta_price*factor

    def price_down(self, factor=0.25):
        self.price_up(factor=-factor)


    def price_span(self, factor=1.25):
        delta_price=self.end_price-self.start_price
        self.start_price+=delta_price*((1-factor)/2)
        self.end_price-=delta_price*((1-factor)/2)


    def date_up(self, factor=0.25):
        delta_date=self.end_date-self.start_date
        self.start_date+=delta_date*factor
        self.end_date+=delta_date*factor

    def date_down(self, factor=0.25):
        self.date_up(factor=-factor)


    def date_span_up(self):
        delta_date=self.end_date-self.start_date
        self.start_date-=delta_date*0.5
        self.end_date+=delta_date*0.5
        self.time_frame*=2
    

    def date_span_down(self):
        if self.time_frame*0.5>=15:
            delta_date=self.end_date-self.start_date
            self.start_date+=delta_date*0.25
            self.end_date-=delta_date*0.25
            self.time_frame*=0.5
    
