def create_exceptions(exception_path, exception_handler_path):
    exception_content = """class ApiException(Exception):

    def __init__(self, error_code):
        self.error_code = error_code
"""

    exception_handler_content = """import traceback
from rest_framework.decorators import api_view
from django.conf import settings
from django.urls.exceptions import Resolver404
from rest_framework.exceptions import (
    MethodNotAllowed,
    ParseError,
    UnsupportedMediaType,
    NotAuthenticated,
    AuthenticationFailed,
    PermissionDenied,
    ValidationError as DRFValidationError,
    Throttled,
)

from .exception import ApiException
from utils import Responder, Constant, Logger


def handle_errors(exception, context):
    error_mappings = {
        ApiException: lambda ex: handle_api_exception(ex),
        MethodNotAllowed: 505,
        Resolver404: 501,
        ParseError: 502,
        PermissionDenied: 506,
        Throttled: 510,
        UnsupportedMediaType: 503,
        NotAuthenticated: 504,
        AuthenticationFailed: 504,
        DRFValidationError: lambda ex: handle_validation_error(ex),
    }
    response_code = error_mappings.get(type(exception), 500)
    if callable(response_code):
        response_code = response_code(exception)

    if isinstance(response_code, list) and (
        response_code["response_code"] == 507 or response_code["response_code"] == 508
    ):
        return Responder.send(response_code["response_code"], data=response_code["data"], status=False)

    if response_code == 500:
        Logger.log(context.get("request"), traceback.format_exc())
        if settings.DEBUG:
            raise exception
    return Responder.send(response_code, status=False)


def handle_api_exception(exception):
    return exception.error_code


def handle_validation_error(exception):
    error_details = exception.detail
    response_code = 507
    data = {}
    for key, val in error_details.items():
        data[key] = str(val[0])
        response_code = Constant.djangoDefaultCodes.get(val[0].code, 507)
    return {
                "response_code": response_code,
                "data": data
            }


@api_view(("GET",))
def handler404(request, exception):
    return Responder.send(501, status=False)
"""

    with open(exception_path, 'w') as file1:
        file1.write(exception_content)
        file1.close()

    with open(exception_handler_path, 'w') as file1:
        file1.write(exception_handler_content)
        file1.close()
