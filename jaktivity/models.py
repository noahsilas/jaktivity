import datetime
from django.db import models
from django.views.generic.base import View
from django.contrib.auth.models import User

class Log(models.Model):

    METHOD_CHOICES = tuple((m.upper(), m.title()) for m in View.http_method_names)

    # request details
    method = models.CharField(max_length=16, choices=METHOD_CHOICES)
    host = models.CharField(max_length=256)
    path = models.CharField(max_length=2048)
    ip_address = models.IPAddressField()
    date = models.DateTimeField(default=datetime.datetime.now)
    user = models.ForeignKey(User, db_index=True, null=True) # null for anon users
    view = models.CharField(max_length=512)

    # response details
    response_status = models.PositiveSmallIntegerField(null=True)
    exception_type = models.CharField(max_length=256, null=True)

    # human readable format
    message = models.CharField(max_length=1024, null=True)

    class Meta:
        permissions = (
            ('can_view_logs', "Can View Logs"),
        )

    def __init__(self, *args, **kwargs):
        super(Log, self).__init__(*args, **kwargs)
        self._notes = []

    def save(self, *args, **kwargs):
        """ Saves the log to DB, as well as any notes that are attached.
        """
        super(Log, self).save(*args, **kwargs)
        for note in self._notes:
            note.log = self
            note.save()
        self._notes = []

    def note(self, text):
        """ Adds a note to this activity log
        """
        if self.pk:
            Note(log=self, body=text).save()
        else:
            self._notes.append(Note(body=text))

    def view_positional_parameters(self):
        return self.view_params.exclude(position=None).order_by('position')

    def view_keyword_parameters(self):
        return self.view_params.exclude(name=None).order_by('name')

    def http_get_parameters(self):
        return self.http_params.filter(method='GET')

    def http_post_parameters(self):
        return self.http_params.filter(method='POST')


class HTTPHeader(models.Model):
    """ Logs HTTP Headers
    """
    log = models.ForeignKey(Log, related_name='headers')
    name = models.CharField(max_length=512)
    value = models.TextField(null=True)


class HTTPParam(models.Model):
    """ Logs HTTP Parameters
    """
    METHOD_CHOICES = (('GET', 'get'), ('POST', 'post'))

    log = models.ForeignKey(Log, related_name="http_params")
    method = models.CharField(max_length=16, choices=METHOD_CHOICES)
    name = models.CharField(max_length=512)
    value = models.TextField(null=True)


class ViewParam(models.Model):
    """ Logs python parameters passed into a view
    """
    log = models.ForeignKey(Log, related_name='view_params')
    position = models.PositiveSmallIntegerField(null=True)
    name = models.CharField(max_length=256, null=True)
    value = models.TextField(null=True)


class Note(models.Model):
    """ User added Notes
    """
    log = models.ForeignKey(Log, related_name='notes')
    body = models.TextField()

