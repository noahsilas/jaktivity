from django.conf.urls.defaults import patterns, url
from jaktivity.views import LogIndex, LogDetail

urlpatterns = patterns('',
    url(r'^$', LogIndex.as_view(), name='index'),
    url(r'^(?P<pk>\d+)$', LogDetail.as_view(), name='detail'),
)
