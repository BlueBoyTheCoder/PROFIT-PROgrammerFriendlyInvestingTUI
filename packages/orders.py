from PASSWORD import *
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, StopLimitOrderRequest, StopOrderRequest, LimitOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce, OrderType
from alpaca.common.exceptions import APIError


class Orders:
    def __init__(self, trading_client: TradingClient):
        self.trading_client = trading_client
        self.symbol = None
        self.qty = 1
        self.side = OrderSide.BUY
        self.type = OrderType.MARKET
        self.time_in_force = TimeInForce.DAY
        self.price = None
        self.current_orders_ids = []

    def update_order(self, symbol=None, qty=None, side=None, type=None, time_in_force=None, price=None):
        if symbol:
            self.symbol = symbol
        if qty:
            self.qty = qty
        if side:
            self.side = side
        if type:
            self.type = type
        if time_in_force:
            self.time_in_force = time_in_force
        if price:
            self.price = price

    def submit_market_order(self):
        """
        Submits market order based on class object attributes values
        """
        order_request = MarketOrderRequest(symbol=self.symbol, qty=self.qty, side=self.side, time_in_force=self.time_in_force)
        try:
            order = self.trading_client.submit_order(order_request)
        except APIError as err:
            return 1

        self.current_orders_ids.append(order.id)

        return 0

    def submit_limit_order(self):
        """
        Submits limit order based on class object attributes values
        """
        order_request = LimitOrderRequest(symbol=self.symbol, qty=self.qty, side=self.side, limit_price=self.price, time_in_force=self.time_in_force)
        try:
            order = self.trading_client.submit_order(order_request)
        except APIError as err:
            return 1

        self.current_orders_ids.append(order.id)

        return 0

    def submit_stop_order(self):
        """
        Submits stop order based on class object attributes values
        """
        order_request = StopOrderRequest(symbol=self.symbol, qty=self.qty, side=self.side, stop_price=self.price, time_in_force=self.time_in_force)
        try:
            order = self.trading_client.submit_order(order_request)
        except APIError as err:
            return 1

        self.current_orders_ids.append(order.id)

        return 0

    def submit_stop_limit_order(self):
        """
        Submits stop limit order based on class object attributes values
        """
        order_request = StopLimitOrderRequest(type=OrderType.STOP_LIMIT, symbol=self.symbol, qty=self.qty, side=self.side, stop_price=self.price, limit_price=self.price, time_in_force=self.time_in_force)
        try:
            order = self.trading_client.submit_order(order_request)
        except APIError as err:
            return 1

        self.current_orders_ids.append(order.id)

        return 0

    def submit_order(self):
        """
        Submits right type of order, based on the type atribute
        """
        match self.type:
            case OrderType.MARKET:
                return self.submit_market_order()
            case OrderType.STOP:
                return self.submit_stop_order()
            case OrderType.LIMIT:
                return self.submit_limit_order()
            case OrderType.STOP_LIMIT:
                return self.submit_stop_limit_order()



def process_order_data(order_list: list[str]):
    """
    Process data needed for updating order attributes
    """
    try:
        order_list[1] = int(order_list[1])

        match order_list[2]:
            case "SELL":
                order_list[2] = OrderSide.SELL
            case _:
                order_list[2] = OrderSide.BUY

        match order_list[3]:
            case "LIMIT":
                order_list[3] = OrderType.LIMIT
            case "STOP":
                order_list[3] = OrderType.STOP
            case "STOP_LIMIT":
                order_list[3] = OrderType.STOP_LIMIT
            case _:
                order_list[3] = OrderType.MARKET

        match order_list[4]:
            case "GTC":
                order_list[4] = TimeInForce.GTC
            case "OPG":
                order_list[4] = TimeInForce.OPG
            case "CLS":
                order_list[4] = TimeInForce.CLS
            case "IOC":
                order_list[4] = TimeInForce.IOC
            case "FOK":
                order_list[4] = TimeInForce.FOK
            case _:
                order_list[4] = TimeInForce.DAY

        order_list[5] = float(order_list[5])

    except (ValueError, IndexError):
        return 1
    return 0