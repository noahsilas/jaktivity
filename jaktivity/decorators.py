import functools
from django.utils.decorators import available_attrs

def log_message(message):
    """ adds a log_message attribute to the wrapped function
    """
    def decorator(func):
        def wrapped_view(*args, **kwargs):
            return func(*args, **kwargs)
        wrapped_view.log_message = message
        wrapper = functools.wraps(func, assigned=available_attrs(func))
        return wrapper(wrapped_view)
    return decorator


def cbv_log_message(message):
    """ adds a log_message to a view inheriting from
        django.views.generic.base.View
    """
    def decorator(view_class):
        view_class.dispatch = log_message(message)(view_class.dispatch)
        return view_class
    return decorator