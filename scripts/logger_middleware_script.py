def create_logger_middleware(logger_path):
    logger_content = '''import time
from utils import Logger


class LoggerMiddleware(object):

    def __init__(self, get_response):
        """
        One-time configuration and initialisation.
        """
        self.startTime = 0
        self.get_response = get_response

    def __call__(self, request):
        """
        Code to be executed for each request before the view (and later
        middleware) are called.
        """
        self.startTime = time.time()
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Called just before Django calls the view.
        """
        return None

    def process_exception(self, request, exception):
        """
        Called when a view raises an exception.
        """
        return None

    def process_template_response(self, request, response):
        """
        Called just after the view has finished executing.
        """
        if response.data.get('code', 500) != 500:
            Logger.log(request, response, round(
                time.time() - self.startTime, 2))
        return response
'''
    with open(logger_path, 'w') as file:
        file.write(logger_content)
