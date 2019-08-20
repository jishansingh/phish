from django.db import models
from django.http.request import split_domain_port
import re
from django.contrib.auth.models import User
# Create your models here.
DOMAINS_CACHE={}
class DomainManager(models.Manager):
    use_in_migrations = True
    def _get_domain_by_id(self, domain_id):
        if domain_id not in DOMAINS_CACHE:
            domain = self.get(pk=domain_id)
            DOMAINS_CACHE[domain_id] = domain
        return DOMAINS_CACHE[domain_id]
    def _get_domain_by_request(self, request):
        host = request.get_host()
        d=re.compile('www.(.*?).example.com')
        d=d.search(host)
        d=d.group(1)
        try:
            if host not in DOMAINS_CACHE:
                DOMAINS_CACHE[host] = self.get(name__icontains=d)
            return DOMAINS_CACHE[host]
        except Website.DoesNotExist:
            domain, port = split_domain_port(host)
            if domain not in DOMAINS_CACHE:
                print(d)
                DOMAINS_CACHE[domain] = self.get(name__icontains=d)
            return DOMAINS_CACHE[domain]
    def get_current(self, request=None, domain_id=None):
        if domain_id:
            return self._get_domain_by_id(domain_id)
        elif request:
            return self._get_domain_by_request(request)
    def clear_cache(self):
        global DOMAINS_CACHE
        DOMAINS_CACHE = {}

class Page(models.Model):
    name=models.URLField()
    code=models.TextField()
    username=models.IntegerField(default=0)
    password=models.IntegerField(default=1)
    index=models.IntegerField(default=0)
    def __str__(self):
        return self.name

class Website(models.Model):
    name=models.CharField(max_length=40)
    pages=models.ManyToManyField(Page)
    objects=DomainManager()
    def __str__(self):
        return self.name
class Hash(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    hash=models.CharField(max_length=20)
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=20)