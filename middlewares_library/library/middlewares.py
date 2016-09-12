from library.models import RequestLog
from django.utils import timezone


class RequestLoggingMiddleware(object):
    """
    Logs each request as a RequestLog model instance. The model will contain
    all details about the request, such as HTTP method, response status
    code, ip, GET and POST params, etc. Follow the fields described in
    the RequestLog model.
    """

    def process_request(self, request):
        request.timestamp = timezone.now()

    def process_response(self, request, response):
        log = RequestLog.objects.create(
            method=request.method,
            code=response.status_code,
            url=request.path,
            full_url=request.get_full_path(),
            ip=request.META.get('REMOTE_ADDR'),
            get_params=request.GET.dict(),
            user_agent=request.META.get('HTTP_USER_AGENT'),
            query_count=0,  # I don't know what this is for
            timestamp=request.timestamp,
            duration_in_seconds=int((timezone.now() - request.timestamp).total_seconds()),
        )
        return response


class SSLRedirectMiddleware(object):
    """
    If the request is not using HTTPS, redirects to the same URL but
    using HTTPS.
    """
    pass


class WWWRedirectMiddleware(object):
    """
    If "www" is included in the URL, redirects to the nacked version
    of the domain (without "www" at the beginning)
    """
    pass


class ExceptionLoggingMiddleware(object):
    """
    Writes a log entry for every exception raised in any request.
    """
    pass
