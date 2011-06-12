""" Simple views to browse captured logs
"""
from django.http import HttpResponseForbidden
from django.views import generic as generic_views

from jaktivity.models import Log

class PermissionMixin(object):

    permissions = ()

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perms(self.permissions):
            return self.permission_denied(request, *args, **kwargs)
        return super(PermissionMixin, self).dispatch(request, *args, **kwargs)

    def permission_denied(self, request, *args, **kwargs):
        """ Called when a view is accessed by a user
            without appropriate permissions.
        """
        return HttpResponseForbidden()

class LogIndex(PermissionMixin, generic_views.ListView):
    """ A list view displaying the most recent log entries
    """
    queryset = Log.objects.all().order_by('-date')
    paginate_by = 100
    permissions = 'jaktivity.can_view_logs'

class LogDetail(PermissionMixin, generic_views.DetailView):
    """ Shows detailed data for a specific log entry
    """
    model = Log
    permissions = 'jaktivity.can_view_logs'
