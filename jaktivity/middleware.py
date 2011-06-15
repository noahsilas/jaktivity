from django.conf import settings
from jaktivity.models import Log, HTTPHeader, HTTPParam, ViewParam

DEFAULT_SAFE_METHODS = ('GET', 'HEAD',)
DEFAULT_SAVE_HEADERS = ()
DEFAULT_IGNORE_PARAMS = ('csrfmiddlewaretoken', 'password',)

class FakeLog(object):
    """ Fakes enough of the Log interface that code expecting a log object
        won't break.
    """
    def __init__(self):
        # fake a Log object's fields to prevent attribute errore
        for name in [field.name for field in Log._meta.fields]:
            setattr(self, name, None)

    def note(self, message):
        return

    def save(self, *args, **kwargs):
        return

    def view_positional_parameters(self):
        return ViewParam.objects.none()

    def view_keyword_parameters(self):
        return ViewParam.objects.none()

    def http_get_parameters(self):
        return HTTPParam.objects.none()

    def http_post_parameters(self):
        return HTTPParam.objects.none()


class ActivityLogMiddleware(object):
    def __init__(self):
        self._safe_methods = getattr(settings, 'JAKTIVITY_SAFE_METHODS', DEFAULT_SAFE_METHODS)
        self._save_headers = getattr(settings, 'JAKTIVITY_SAVE_HEADERS', DEFAULT_SAVE_HEADERS)
        self._ignore_params = getattr(settings, 'JAKTIVITY_IGNORE_PARAMS', DEFAULT_IGNORE_PARAMS)

    def save_headers(self, request):
        """ Saves HTTPHeader records
        """
        for header in self._save_headers:
            if header in request.META:
                hdr = HTTPHeader(log=request.log)
                hdr.name = header
                hdr.value = request.META[header]
                hdr.save()

    def save_params(self, request, method):
        """ Saves HTTP Parameters
        """
        params = getattr(request, method, [])
        for param in params:
            if param.lower() in self._ignore_params:
                continue
            for value in params.getlist(param):
                prm = HTTPParam(log=request.log, method=method)
                prm.name = param
                prm.value = value
                prm.save()

    def save_view_info(self, request, view_func, view_args, view_kwargs):
        """ Saves information about the view being called and its parameters
        """
        request.log.view = '.'.join((view_func.__module__, view_func.__name__))
        for index, arg in enumerate(view_args):
            prm = ViewParam(log=request.log)
            prm.position = index
            prm.value = arg
            prm.save()

        for name, value in view_kwargs.iteritems():
            prm = ViewParam(log=request.log)
            prm.name = name
            prm.value = value
            prm.save()

    def make_message(self, request, view_func, view_args, view_kwargs):
        """ Tries to make a log message for a view
        """
        try:
            message = view_func.log_message
        except AttributeError:
            message = None
        if message:
            if callable(message):
                request.log.message = message(request, *view_args, **view_kwargs)
            else:
                request.log.message = message

    def process_view(self, request, view_func, view_args, view_kwargs):
        """ Called before the view function
        """
        if getattr(view_func, 'log_always', False):
            # the view is marked to always be logged. Skip the rest of the
            # rulechain.
            pass
        elif getattr(view_func, 'log_never', False):
            # the view is marked to never be logged. Stop.
            request.log = FakeLog()
            return
        elif request.method in self._safe_methods:
            # we are viewing this page with a safe method: we don't
            # need to log this request.
            request.log = FakeLog()
            return

        ### setup the log object
        request.log = Log()
        request.log.method = request.method
        request.log.host = request.get_host()
        request.log.path = request.path
        request.log.ip_address = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
        if request.user.is_authenticated():
            request.log.user = request.user

        request.log.save()

        self.save_headers(request)
        self.save_params(request, 'GET')
        self.save_params(request, 'POST')
        self.save_view_info(request, view_func, view_args, view_kwargs)
        self.make_message(request, view_func, view_args, view_kwargs)


    def process_response(self, request, response):
        """ Called on a successful response
        """
        if not hasattr(request, 'log'):
            return response

        request.log.response_status = response.status_code
        request.log.save()
        return response

    def process_exception(self, request, exception):
        """ Called when the view has generated an exception
        """
        if not hasattr(request, 'log'):
            return

        exc_type = type(exception)
        exc_path = "%s.%s" % (exc_type.__module__, exc_type.__name__)
        request.log.exception_type = exc_path
        request.log.note(str(exception))
        request.log.save()