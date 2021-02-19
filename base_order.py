class BaseOrder(object):
    
    def __init__(self, instruction, symbol, quantity, order_type="MARKET", asset_type="EQUITY",
                 duration="DAY", session="NORMAL", order_strategy_type="SINGLE"):
        self.instruction = instruction
        self.symbol = symbol
        self.quantity = quantity
        self.order_type = order_type
        self.asset_type = asset_type
        self.duration = duration
        self.session = session
        self.order_strategy_type = order_strategy_type

    def build(self):
        order = {
            "orderType": self.order_type,
            "session": self.session,
            "duration": self.duration,
            "orderStrategyType": self.order_strategy_type,
            "orderLegCollection": [
                {
                    "instruction": self.instruction,
                    "quantity": self.quantity,
                    "instrument": {
                        "symbol": self.symbol,
                        "assetType": self.asset_type}}]}
        return order
    
    """
    FUTURE WAY TO BUILD ORDER
    # build instrument dict
    instrument = {"symbol": self.symbol, "asset"}


    order = {"session": self.session}
    order["duration"] = self.duration
    order["orderType"] = self.order_type
    order["orderStrategyType"] = self.order_strategy_type
    order["duration"] = self.duration
    order["duration"] = self.duration
    """
