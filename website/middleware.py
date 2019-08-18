from django.utils.deprecation import MiddlewareMixin
from .models import Website
class CurrentDomainMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.domain = Website.objects.get_current(request)