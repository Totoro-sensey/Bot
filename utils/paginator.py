import math
from data.config import PAGE


class Paginator:

    def __init__(self, obj_list, page_number=1, diapason=0):
        self.page_number = page_number
        self.diapason = diapason
        self.page = self.get_page(obj_list)

    def get_page(self, obj_list, page_number=1):
        self.diapason = math.ceil(len(obj_list)/PAGE)
        self.page = obj_list[PAGE * (page_number - 1):page_number*PAGE]
        self.page_number = page_number
        return self.page

    def has_next(self, page_number):
        return 1 <= page_number <= self.diapason

    def has_previous(self, page_number):
        return self.diapason >= page_number >= 1
