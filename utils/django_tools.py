# encoding: utf-8

from rest_framework.pagination import PageNumberPagination

class NoPagination(PageNumberPagination):
    page_size = 99999 # Said the number of the default display per page
    page_size_query_param = 'page_size' # Each page number in the url parameter
    page_query_param = 'p' # Said the url of the page parameter
    max_page_size = 99999  # Said the biggest display number each page, do restrictions on the use, avoid sudden large amounts of data query, database crash
