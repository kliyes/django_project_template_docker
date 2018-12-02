from logging import getLogger

from django.utils.deprecation import MiddlewareMixin


logger = getLogger("error_file")


class ErrorLoggingMiddleware(MiddlewareMixin):

    def process_exception(self, request, exception):
        logger.exception(exception)
