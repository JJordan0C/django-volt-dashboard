import re
from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from django.utils.http import url_has_allowed_host_and_scheme

EXEMPT_URLS = [re.compile(settings.LOGIN_URL.lstrip('/'))]

class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        assert hasattr(request, 'user'), "The Login Required Middleware"
        if not request.user.is_authenticated:
            path = request.path_info.lstrip('/')
            if not any(m.match(path) for m in EXEMPT_URLS):
                redirect_to = settings.LOGIN_URL
                if len(path) > 0 and url_has_allowed_host_and_scheme(
                    url=request.path_info, allowed_hosts=request.get_host()):
                    redirect_to = f"{settings.LOGIN_URL}"

                    return HttpResponseRedirect(redirect_to)