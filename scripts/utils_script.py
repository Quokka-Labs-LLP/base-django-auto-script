import os


def create_utils(utils_path, project_name):
    responder_content = """from .constants import Constant
from rest_framework.response import Response
from django.http import HttpResponse
from django_base_architecture.exception import ApiException


class Responder:

    @staticmethod
    def send(code, data=None, status=True):
        return Response(
            {
                "status": status,
                "code": code,
                "message": Constant.response_messages[code],
                "data": data if data is not None else {},
            },
            status=200 if status else 400
        )

    @staticmethod
    def sendText(code):
        return HttpResponse(Constant.response_messages[code])

    @staticmethod
    def raiseError(code):
        raise ApiException(code)
"""
    responder_content = responder_content.replace("django_base_architecture", project_name)

    logger_content = '''from django.utils.timezone import localtime
from django.conf import settings
from loguru import logger
from .constants import Constant
from pytz import timezone
from .helper import Helper


class Logger:
    base_path = f'{settings.BASE_DIR}/logs/{{time:YYYY}}/{{time:MMMM}}/{{time:DD}}'

    logger.add(
        f'{base_path}/request.log', format="{message}", rotation="1 days", level="INFO",
        filter=Helper.log_filter("request")
    )
    logger.add(
        f'{base_path}/error.log', format="{message}", rotation="1 days", level="INFO",
        filter=Helper.log_filter("error")
    )
    logger.add(
        f'{base_path}/custom.log', format="{message}", rotation="1 days", level="INFO",
        filter=Helper.log_filter("custom")
    )

    request_log = logger.bind(name="request")
    error_log = logger.bind(name="error")
    custom_log = logger.bind(name="custom")

    @classmethod
    def log(cls, request, response, time_taken=None):
        if settings.DEBUG:
            return None
        current_time = localtime(timezone=timezone(
            "Asia/Kolkata")).strftime("%I:%M:%S %p (%Z)")
        data = f"""
            {current_time} | IP [{request.META.get('REMOTE_ADDR')}]
            {request.build_absolute_uri()} ({request.method})
            HEADERS {request.headers}\\n"""
        if time_taken is not None:
            data += f"""STATUS [{response.data.get('status')}] | STATUS_CODE [{response.data.get('code')} ~ {Constant.response_messages[response.data.get('code')]}] | TIME_TAKEN [{round(time_taken, 3)} Seconds]\\n"""     # noqa
            data += "\\n************************************************************************************************************"   # noqa
            cls.request_log.info(data.replace('  ', ''))
        else:
            data += f"""STATUS [False] | STATUS_CODE [500 ~ Server Error]

            xxxxxxxxxxxxxxxxxxxx [ERROR] xxxxxxxxxxxxxxxxxxxxxxxxxx
            {response}"""
            data += "\\n************************************************************************************************************"   # noqa
            cls.error_log.info(data.replace('  ', ''))

    @classmethod
    def custom(cls, request, output):
        current_time = localtime(timezone=timezone(
            "Asia/Kolkata")).strftime("%I:%M:%S %p (%Z)")
        data = f"""
            {current_time} | IP [{request.META.get('REMOTE_ADDR')}]
            {request.build_absolute_uri()} ({request.method})
            HEADERS {request.headers}\\n
            ************************************************************************************************************
            {output}
            \\n************************************************************************************************************\\n
            """
        cls.custom_log.info(data.replace('  ', ''))
'''
    helper_content = """class Helper:

    def log_filter(name):
        def filter(record):
            return record['extra'].get('name') == name
        return filter
"""

    constants_content = """class Constant:

    django_default_codes = {
        "required": 508,
        "blank": 508,
        "null": 508,
        "empty": 508,
    }

    response_messages = {
        500: "Internal server error.",
        501: "The requested API endpoint is not valid.",
        502: "The provided data is not in a valid JSON format.",
        503: "The 'Content-Type' header should be set to 'application/json'.",
        504: "User authentication failed.",
        505: "The requested HTTP method is not allowed.",
        506: "Sorry, you are not authorized to perform this action.",
        507: "Invalid parameter value provided.",
        508: "Required parameter or value is missing.",
        509: "User access token is expired or invalid.",
        510: "Your daily quota has been exhausted. Please try again later.",

        100: "wrking"
    }
"""

    init_content = """from .responder import Responder  # noqa
from .constants import Constant   # noqa
from .logger import Logger        # noqa
from .helper import Helper        # noqa
"""

    with open(os.path.join(utils_path, '__init__.py'), 'w') as file:
        file.write(init_content)

    with open(os.path.join(utils_path, 'constants.py'), 'w') as file:
        file.write(constants_content)

    with open(os.path.join(utils_path, 'helper.py'), 'w') as file:
        file.write(helper_content)

    with open(os.path.join(utils_path, 'logger.py'), 'w') as file:
        file.write(logger_content)

    with open(os.path.join(utils_path, 'responder.py'), 'w') as file:
        file.write(responder_content)
