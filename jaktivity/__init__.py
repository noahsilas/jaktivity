"""
To add logging to a class based view:

from django.views.generic.base import View
from jaktivity.decorators import cbv_log_message

@cbv_log_message('MyView hit!')
class MyView(View):
    ...
    
"""