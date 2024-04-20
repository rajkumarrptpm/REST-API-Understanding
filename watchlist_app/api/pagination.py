#pageNumberPagination
from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination

class WatchlistPagination(PageNumberPagination):
     page_size = 2
     page_query_param = 'P' # used to change the name in url default is page
     page_size_query_param = 'size'
     max_page_size = 10
     last_page_strings = 'end'

class WatchlistLOPagination(LimitOffsetPagination):
     default_limit = 2
     max_limit = 10
