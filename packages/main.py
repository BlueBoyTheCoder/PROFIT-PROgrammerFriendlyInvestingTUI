from client import Client
from chart import Chart
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta, timezone

def print_dict(dict):
    for d in dict:
        print(d)

def main():
    client = Client()
    utc_m4 = timezone(timedelta(hours=-4))

    # data = client.get_data("SPY",datetime.now(utc_m4)-timedelta(weeks=1),datetime.now(utc_m4)-timedelta(days=1),TimeFrame.Hour)
    # print_dict(data)

    # data = client.get_data("SPY",datetime.now(utc_m4)-timedelta(hours=11),datetime.now(utc_m4)-timedelta(hours=10),TimeFrame.Minute)
    # print_dict(data)

    # data = client.get_newest_data("SPY")
    # print(data)

    chart = Chart()
    chart.update(uuid='SPY')
    chart.reload()
    #print(chart.get_params())

    #print_dict(chart.get_data())

    print(chart.get_instruments_data())
    chart.add_instrument('SPY')
    print(chart.get_instruments_data())
    chart.add_instrument('AAPL')
    print(chart.get_instruments_data())
    chart.reload_instruments()
    print(chart.get_instruments_data())

if __name__ == "__main__":
    main()