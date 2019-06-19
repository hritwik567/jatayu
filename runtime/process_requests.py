from lru import *

# Create this class object and invoke process_requests function with uuid parameter
class ProcessRequests:

    def __init__(self):
        self.lru_cache = LRUCache()

    def process_requests(self, request_name):
        self.lru_cache.insertItem(request_name)
        cleanup_list = self.lru_cache.validateItem()
        print(self.lru_cache.item_list)
        return cleanup_list

    def delete_requests(self, request_name):
        self.lru_cache.removeItem(request_name)
