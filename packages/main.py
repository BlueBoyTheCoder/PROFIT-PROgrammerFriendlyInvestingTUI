from client import Client
from chart import Chart
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta, timezone
from exceptions import *



def main():
    client = Client()
    chart = Chart()
    utc_m4 = timezone(timedelta(hours=-4))

    def print_list(lista):
        for l in lista:
            print(l)
    
    def print_dict(dic):
        for d in dic:
            print(d, dic[d])

    print(dict(client.client.get_asset("SPY"))['name'])

    data = client.get_historical_data("AAPL",datetime.now(utc_m4)-timedelta(days=10),datetime.now(utc_m4)-timedelta(days=1),TimeFrame.Hour)
    print_list(data)

    data = client.get_historical_data("SPY",datetime.now(utc_m4)-timedelta(hours=11),datetime.now(utc_m4)-timedelta(hours=10),TimeFrame.Minute)
    print_list(data)

    data = client.get_lastday_data("AAPL")
    print_list(data)

    data = client.get_newest_data("AAPL")
    print_list(data)

    data = client.get_newest_data("SPY")
    print(data)

    print(client.get_client_status())

    print(client.get_client_positions())

    chart.update(uuid='SPY')
    chart.reload()
    print(chart.get_params())

    print_list(chart.get_data())

    print(chart.get_instruments_data())
    chart.add_instrument('SPY')
    print(chart.get_instruments_data())
    chart.add_instrument('AAPL')
    print(chart.get_instruments_data())
    chart.reload_instruments()
    print_dict(chart.get_instruments_data())

if __name__ == "__main__":
    main()