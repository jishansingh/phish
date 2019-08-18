from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns('',
    host(r'main', settings.ROOT_URLCONF, name='main'),
    host(r'(?!www)\w+', 'website.urls', name='wildcard'),
)
