from django.conf import settings

from .models import AccessLog


class AccessLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if self.should_log(request):
            AccessLog.objects.create(
                method=request.method,
                path=request.get_full_path()[:500],
                status_code=response.status_code,
                user=request.user if request.user.is_authenticated else None,
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:1000],
                referer=request.META.get('HTTP_REFERER', '')[:500],
            )

        return response

    def should_log(self, request):
        path = request.path
        ignored_prefixes = (
            f'/{settings.STATIC_URL.strip("/")}/',
            f'/{settings.MEDIA_URL.strip("/")}/',
            '/favicon.ico',
        )
        return not path.startswith(ignored_prefixes)

    def get_client_ip(self, request):
        forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if forwarded_for:
            return forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')
