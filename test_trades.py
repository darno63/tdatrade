from base_order import BaseOrder
from trades_api import save_order, get_orders

walmart_order = BaseOrder(instruction="BUY", symbol="WMT", quantity=1).build()

#to_cancel = get_orders()
#save_order(walmart_order)

order_id = get_orders()

get_orders(order_id)

#print(to_cancel)
