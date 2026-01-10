import logging

from ipware import get_client_ip

from django.core.handlers.wsgi import WSGIRequest

__all__ = ["RequestLoggingMiddleware"]

logger = logging.getLogger("django.request")


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: WSGIRequest):
        response = self.get_response(request)

        extra = {
            "real_client_ip": None,
            #
            "is_succeeded": 200 <= response.status_code < 300,
            "status_code": response.status_code,
            "method": request.method.lower(),
            "path": request.path or request.path_info,
            #
            "user_id": None,
        }
        if hasattr(request, "user") and request.user.is_authenticated:
            extra["user_id"] = request.user.id

        client_ip, is_routable = get_client_ip(request)
        if is_routable:
            extra["real_client_ip"] = client_ip

        logger.info(f"{response.status_code} {request.method} {request.build_absolute_uri()}", extra=extra)

        return response

