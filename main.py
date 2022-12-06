import xml.etree.ElementTree as ET

tree = ET.parse('orders.xml')
root = tree.getroot()


class Book:
    def init(self, name):
        self.name = name
        self.buy_buks = []  # max heap
        self.sell_buks = []  # min heap


time = 0
buk = {}

for son in root:
    # add time to each ord
    son.attrib['Time'] = time
    buks = son.attrib['book']
    price = float(son.attrib['price'])
    op = son.attrib['operation']
    vol = float(son.attrib['volume'])
    time += 1
    if buks not in buk:
        buk[buks] = Book(buks)
    if son.tag == 'DeleteOrder':
        if son.attrib['operation'] == 'SELL':
            buk[buks].sell_buks.remove(son.attrib['orderId'])
        else:
            buk[buks].buy_buks.remove(son.attrib['orderId'])
    else:
        if son.attrib['operation'] == 'SELL':
            for ord in buk[buks].buy_buks:
                if float(ord.attrib['price']) >= price:
                    if ord.attrib['volume'] > vol:
                        ord.attrib['volume'] -= vol
                        vol = 0
                    else:
                        vol -= int(ord.attrib['volume'])
                        buk[buks].buy_buks.remove(ord)
                        # sort by price
                        buk[buks].buy_buks.sort(key=lambda x: float(x.attrib['price']), reverse=True)
                else:
                    break
            if vol > 0:
                son.attrib['volume'] = vol
                buk[buks].sell_buks.append(son)
                # sort by price
                buk[buks].sell_buks.sort(key=lambda x: float(x.attrib['price']))
                break
        else:
            for ord in buk[buks].sell_buks:
                if float(ord.attrib['price']) <= price:
                    if ord.attrib['volume'] > vol:
                        ord.attrib['volume'] -= vol
                        vol = 0
                    else:
                        vol -= int(ord.attrib['volume'])
                        buk[buks].sell_buks.remove(ord)
                        # sort by price
                        buk[buks].sell_buks.sort(key=lambda x: float(x.attrib['price']))
                else:
                    break
            if vol > 0:
                son.attrib['volume'] = vol
                buk[buks].buy_buks.append(son)
                # sort by price
                buk[buks].buy_buks.sort(key=lambda x: float(x.attrib['price']), reverse=True)
                break
#
# We can keep a dictionary of the ord buk that map to the maxheap and minheap for purchase ords and sell ords, respectively. The ord buks now has a second dictionary of ordIDs.
# When an ord is received, if it is a delete ord, we look for it in the ord buks's piles and, if we find it, delete it.
# If it is an addord, we add to the add ord heap and continue deleting ords from both buk until the condition is satisfied. This is done until the price at the top of the sale buks is less than the top of the purchase buks.
