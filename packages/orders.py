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
        if symbol: self.symbol = symbol
        if qty: self.qty = qty
        if side: self.side = side
        if type: self.type = type
        if time_in_force: self.time_in_force = time_in_force
        if price: self.price = price


    def submit_market_order(self):
        order_request = MarketOrderRequest(
                            symbol=self.symbol,
                            qty=self.qty,
                            side=self.side,
                            time_in_force=self.time_in_force)
        try:
            order = self.trading_client.submit_order(order_request)
        except APIError as err:
            return err.message

        self.current_orders_ids.append(order.id)

        return 0


    def submit_limit_order(self):
        order_request = LimitOrderRequest(
                            symbol=self.symbol,
                            qty=self.qty,
                            side=self.side,
                            limit_price=self.price,
                            time_in_force=self.time_in_force)
        try:
            order = self.trading_client.submit_order(order_request)
        except APIError as err:
            return err.message

        self.current_orders_ids.append(order.id)

        return 0


    def submit_stop_order(self):
        order_request = StopOrderRequest(
                            symbol=self.symbol,
                            qty=self.qty,
                            side=self.side,
                            stop_price=self.price,
                            time_in_force=self.time_in_force)
        try:
            order = self.trading_client.submit_order(order_request)
        except APIError as err:
            return err.message

        self.current_orders_ids.append(order.id)

        return 0


    def submit_stop_limit_order(self):
        order_request = StopLimitOrderRequest(
                            type=OrderType.STOP_LIMIT,
                            symbol=self.symbol,
                            qty=self.qty,
                            side=self.side,
                            stop_price=self.price,
                            limit_price=self.price,
                            time_in_force=self.time_in_force)
        try:
            order = self.trading_client.submit_order(order_request)
        except APIError as err:
            return err.message

        self.current_orders_ids.append(order.id)

        return 0


    def submit_order(self):
        match self.type:
            case OrderType.MARKET:
                return self.submit_market_order()
            case OrderType.STOP:
                return self.submit_stop_order()
            case OrderType.LIMIT:
                return self.submit_limit_order()
            case OrderType.STOP_LIMIT:
                return self.submit_stop_limit_order()
