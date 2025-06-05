from chart import *
from datetime import timedelta, timezone
from timeframeint import TimeFrameInt
import curses
import time


class ChartDisplay(Chart):
    def __init__(self, uuid=0, time_frame=30, height=15, width=60, start_date=None, end_date=None, start_price=None, end_price=None):
        """
        Initialize atributes of class object
        If start_price is not None then it choose reasonable frame size for chart 
        """
        self.chart = None
        self.chart_available = True
        self.place_for_data = 4
        self.place_for_price = 7
        self.price = None
        self.current_data = False  # False when data needs to be updated
        self.pending_uuid = None  # False when uuid needs to be updated, after current operations

        if start_price == None:
            self.reload()
            self.start_price = float("inf")
            self.end_price = -float("inf")
            for d in self.data:
                self.start_price = min(d["open"], self.start_price)
                self.end_price = max(d["open"], self.end_price)
            self.data = None
            price_delta = self.end_price - self.start_price
            self.start_price -= price_delta * 0.5
            self.end_price += price_delta * 0.5
        else:
            self.start_price = start_price
            self.end_price = end_price

        super().__init__(uuid, time_frame, height, width, start_date, end_date)

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

    def uncurrent_data(self):
        self.current_data = False

    def set_pending_uuid(self, uuid):
        """
        Sets atributes, so create_chart method will
        update uuid when used
        """
        if self.client.uuid_exists(uuid):
            self.pending_uuid = uuid
            self.uncurrent_data()

    def create_chart(self):
        """
        Creates chart when it does not have current data
        Gets useful information from data to create chart (self.chart)
        that is used to visualize chart
        """
        if self.current_data:
            return
        if self.pending_uuid:
            self.uuid = self.pending_uuid
            self.pending_uuid = None
            self.reload()
            self.start_price = float("inf")
            self.end_price = -float("inf")
            for d in self.data:
                self.start_price = min(d["open"], self.start_price)
                self.end_price = max(d["open"], self.end_price)
            self.data = None
            price_delta = self.end_price - self.start_price
            self.start_price -= price_delta * 0.5
            self.end_price += price_delta * 0.5

        self.reload()

        chart = [dict() for _ in range(self.width - self.place_for_price)]

        self.price = round(self.get_current_price(), 2)

        price = []

        for d in self.data:
            if self.time_frame >= 1920:
                price.append((d["open"], d["close"], d["timestamp"].replace(hour=0), 1))
            else:
                price.append((d["open"], d["close"], d["timestamp"], 1))

        price_max = self.end_price
        price_min = self.start_price
        price_delta = price_max - price_min

        price_step = price_delta / (self.height - self.place_for_data)

        date = price[0][2]
        date = self.start_date
        date = date.replace(tzinfo=timezone.utc)

        subparts = 0
        match TimeFrameInt(self.time_frame):
            case TimeFrameInt.M15 | TimeFrameInt.M30:
                subparts = self.time_frame
                time_step = timedelta(minutes=1)
                date = date.replace(second=0, microsecond=0)

            case TimeFrameInt.H1:
                subparts = 1
                time_step = timedelta(hours=1)
                date = date.replace(minute=0, second=0, microsecond=0)

            case TimeFrameInt.H2 | TimeFrameInt.H4 | TimeFrameInt.H8 | TimeFrameInt.H16:
                subparts = self.time_frame // 60
                time_step = timedelta(hours=1)
                date = date.replace(minute=0, second=0, microsecond=0)

            case TimeFrameInt.D2 | TimeFrameInt.D4 | TimeFrameInt.D8 | TimeFrameInt.D16 | TimeFrameInt.D32 | TimeFrameInt.D64:
                subparts = self.time_frame // 1920
                time_step = timedelta(days=1)
                date = date.replace(hour=0, minute=0, second=0, microsecond=0)

            case _:
                return

        i_ = 0
        price_start, price_end = 0, 0
        for i in range(0, (self.width - self.place_for_price) * subparts, subparts):
            start = float("inf")
            end = -float("inf")
            for k in range(i, i + subparts):
                if k - i_ >= len(price):
                    break

                if price[k - i_][2] == date + k * time_step:
                    p = price[k - i_]
                    if start == float("inf"):
                        price_start = p[0]
                        start = int((p[0] - price_min) / price_step)
                    price_end = p[1]
                    end = int((p[1] - price_min) / price_step)

                else:
                    i_ += 1

            if start != float("inf"):
                chart[i // subparts]["start"] = min(start, end)
                chart[i // subparts]["length"] = max(1, abs(end - start))
                if price_start < price_end:
                    chart[i // subparts]["direction"] = 1
                else:
                    chart[i // subparts]["direction"] = -1
            else:

                chart[i // subparts]["start"] = 0
                chart[i // subparts]["length"] = 0
                chart[i // subparts]["direction"] = 1

            chart[i // subparts]["date"] = date + i * time_step

        self.chart_available = False
        self.chart = chart
        self.current_data = True
        self.chart_available = True

    def display_chart(self, stdscr, y, x):
        """
        Method that uses curses to visualize chart
        created when create_chart method used
        """
        if self.chart == None or self.chart_available == False:
            return -1
        else:
            for i, ch in enumerate(self.chart):
                if ch["direction"] == 1:
                    color = 1
                else:
                    color = 2
                for j in range(ch["start"], ch["start"] + ch["length"]):
                    if j >= 0 and self.height - j - self.place_for_data >= 0:
                        stdscr.attron(curses.color_pair(color))
                        stdscr.addstr(y + self.height - j - self.place_for_data, x + i, "#")
                        stdscr.attroff(curses.color_pair(color))

                if i % 20 == 0:
                    stdscr.addstr(y + self.height - self.place_for_data + 1, x + i, "|")
                    stdscr.addstr(y + self.height - self.place_for_data + 2, x + i, str(ch["date"].time()))
                    stdscr.addstr(y + self.height - self.place_for_data + 3, x + i, str(ch["date"].date()))

            for i in range(self.height - self.place_for_data):
                delta_price = (self.end_price - self.start_price) / (self.height - self.place_for_data)
                if i % 10 == 0:
                    stdscr.addstr(y + self.height - i - self.place_for_data, x + self.width - self.place_for_price, "-")
                    stdscr.addstr(y + self.height - i - self.place_for_data, x + self.width - self.place_for_price + 2, str(round(self.start_price + delta_price * i, 1)))
        stdscr.refresh()

    def price_up(self, factor=0.25):
        """
        moves price range up by a factor
        """
        delta_price = self.end_price - self.start_price
        self.start_price += delta_price * factor
        self.end_price += delta_price * factor

    def price_down(self, factor=0.25):
        """
        moves price range down by a factor
        """
        self.price_up(factor=-factor)

    def price_span(self, factor=1.25):
        """
        changes price spam by a factor
        """
        delta_price = self.end_price - self.start_price
        self.start_price += delta_price * ((1 - factor) / 2)
        self.end_price -= delta_price * ((1 - factor) / 2)

    def date_up(self, factor=0.25):
        """
        moves date range up by a factor
        """
        delta_date = self.end_date - self.start_date
        self.start_date += delta_date * factor
        self.end_date += delta_date * factor

    def date_down(self, factor=0.25):
        """
        moves date range down by a factor
        """
        self.date_up(factor=-factor)

    def date_span_up(self):
        """
        decrease date span by half
        """
        if self.time_frame < 61440:
            delta_date = self.end_date - self.start_date
            self.start_date -= delta_date * 0.5
            self.end_date += delta_date * 0.5
            self.time_frame *= 2

    def date_span_down(self):
        """
        increase date span twice
        """
        if self.time_frame > 15:
            delta_date = self.end_date - self.start_date
            self.start_date += delta_date * 0.25
            self.end_date -= delta_date * 0.25
            self.time_frame *= 0.5
