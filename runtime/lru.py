from datetime import datetime
from collections import OrderedDict
class LRUCache(object):
    """A sample class that implements LRU algorithm"""

    def __init__(self, delta=300):
        self.delta = delta
        self.item_list = {}

    def insertItem(self, item):
        """Insert new items to cache"""

        if item in self.item_list:
            # Move the existing item to the head of item_list.
            self.item_list[item] = datetime.now()
            print ("tuple added :{0}".format(item))
        else:
            # If this is a new item, just append it to
            # the front of item_list.
            self.item_list[item]=datetime.now()
            self.item_list = OrderedDict(sorted(self.item_list.items(), key=lambda t: t[0]))
            print ("tuple added :{0}".format(item))

    def removeItem(self, item):
        """Remove those invalid items"""
        del self.item_list[item]

    def validateItem(self):
        """Check if the items are still valid."""
        list = []
        now = datetime.now()
        for item in self.item_list:
            time_delta = now - self.item_list[item]
            print ("time delta is :{0}".format(time_delta))
            if time_delta.seconds > self.delta:
                list += [item]
                print ("deleted item is : {0}".format(item))
                print ("send signal to main to delete the deployment")

        for item in list:
            self.removeItem(item) #del self.item_list[item]    
        return list
