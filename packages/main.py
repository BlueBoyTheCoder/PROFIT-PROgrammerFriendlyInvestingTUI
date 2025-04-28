from client import Client
from chart import Chart
from orders import Orders
from widget import Widget
from alpaca.data.timeframe import TimeFrame
from alpaca.trading.enums import OrderSide, TimeInForce, OrderType
from datetime import datetime, timedelta, timezone
from exceptions import *
from alpaca.common.exceptions import APIError



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

    # print(dict(client.client.get_asset("SPY"))['name'])

    # data = client.get_historical_data("AAPL",datetime.now(utc_m4)-timedelta(days=10),datetime.now(utc_m4)-timedelta(days=1),TimeFrame.Hour)
    # print_list(data)

    # data = client.get_historical_data("SPY",datetime.now(utc_m4)-timedelta(hours=25),datetime.now(utc_m4)-timedelta(hours=24),TimeFrame.Minute)
    # print_list(data)

    data = client.get_lastday_data("AAPL")
    print_list(data)

    data = client.get_newest_data("AAPL")
    print_list(data)

    data = client.get_newest_data("SPY")
    print(data)

    # print(client.get_client_status())

    # print(client.get_client_positions())

    # chart.update(uuid='SPY')
    # chart.reload()
    # print(chart.get_params())

    # print_list(chart.get_data())

    # print(chart.get_instruments_data())
    # chart.add_instrument('SPY')
    # print(chart.get_instruments_data())
    # chart.add_instrument('AAPL')
    # print(chart.get_instruments_data())
    # chart.reload_instruments()
    # print_dict(chart.get_instruments_data())

    # orders = Orders(client.get_trading_client())
    # orders.update_order(symbol="SPY")
    # orders.submit_order()
    # orders.update_order(symbol="AAPL",qty=3,side=OrderSide.SELL)
    # try:
    #     orders.submit_order()
    # except APIError as err:
    #     print(err.message)


    w=Widget(['AAPL','SPY','AAA'])
    print(w.instruments)
    w.add_instrument('B')
    print(w.instruments)
    w.add_instrument(['C'])
    print(w.instruments)
    w.pop_instrument(['B','AAA','C'])
    print(w.instruments)
    w.reload_instruments()
    print(w.instruments)
    import time
    for i in range(8):
        time.sleep(1)
        w.reload_instruments()
        print(w.instruments)


if __name__ == "__main__":
    main()