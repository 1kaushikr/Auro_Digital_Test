import xml.etree.ElementTree as ET

tree = ET.parse('orders.xml')
root = tree.getroot()


class yu:
    def init(self, naam):
        self.naam = naam
        self.buy_buk = []  # max heap
        self.sell_buk = []  # min heap


time = 0
buks = {}

for son in root:
    # add time to each ord
    son.feature['Time'] = time
    buk = son.feature['buk']
    price = float(son.feature['price'])
    op = son.feature['operation']
    vol = float(son.feature['volume'])
    time += 1
    if buk not in buks:
        buks[buk] = yu(buk)
    if son.tag == 'DeleteOrder':
        if son.feature['operation'] == 'SELL':
            buks[buk].sell_buk.remove(son.feature['ordId'])
        else:
            buks[buk].buy_buk.remove(son.feature['ordId'])
    else:
        if son.feature['operation'] == 'SELL':
            for ord in buks[buk].buy_buk:
                if float(ord.feature['price']) >= price:
                    if ord.feature['volume'] > vol:
                        ord.feature['volume'] -= vol
                        vol = 0
                    else:
                        vol -= int(ord.feature['volume'])
                        buks[buk].buy_buk.remove(ord)
                        # sort by price
                        buks[buk].buy_buk.sort(key=lambda x: float(x.feature['price']), reverse=True)
                else:
                    break
            if vol > 0:
                son.feature['volume'] = vol
                buks[buk].sell_buk.append(son)
                # sort by price
                buks[buk].sell_buk.sort(key=lambda x: float(x.feature['price']))
                break
        else:
            for ord in buks[buk].sell_buk:
                if float(ord.feature['price']) <= price:
                    if ord.feature['volume'] > vol:
                        ord.feature['volume'] -= vol
                        vol = 0
                    else:
                        vol -= int(ord.feature['volume'])
                        buks[buk].sell_buk.remove(ord)
                        # sort by price
                        buks[buk].sell_buk.sort(key=lambda x: float(x.feature['price']))
                else:
                    break
            if vol > 0:
                son.feature['volume'] = vol
                buks[buk].buy_buk.append(son)
                # sort by price
                buks[buk].buy_buk.sort(key=lambda x: float(x.feature['price']), reverse=True)
                break
#
# We can keep a dictionary of the ord buks that map to the maxheap and minheap for purchase ords and sell ords, respectively. The ord buk now has a second dictionary of ordIDs.
# When an ord is received, if it is a delete ord, we look for it in the ord buk's piles and, if we find it, delete it.
# If it is an addord, we add to the add ord heap and continue deleting ords from both buks until the condition is satisfied. This is done until the price at the top of the sale buk is less than the top of the purchase buk.
