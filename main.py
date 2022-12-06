import xml.etree.ElementTree as ET
import heapq
tree = ET.parse('orders.xml')
root = tree.getroot()

#
# We can keep a dictionary of the order books that map to the maxheap and minheap for purchase orders and sell orders, respectively. The order book now has a second dictionary of orderIDs.
# When an order is received, if it is a delete order, we look for it in the order book's piles and, if we find it, delete it.
# If it is an addorder, we add to the add order heap and continue deleting orders from both books until the condition is satisfied. This is done until the price at the top of the sale book is less than the top of the purchase book.