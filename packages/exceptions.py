class InvalidKey(Exception):
    def __init__(self, message="Your API_KEY or SECRET_KEY is invalid"):
        super().__init__(message)



class InvalidAssetClass(Exception):
    def __init__(self, message="Your financial instrument class is invalid"):
        super().__init__(message)



class InvalidOrderData(Exception):
    def __init__(self, message="Your order has incorrect data"):
        super().__init__(message)