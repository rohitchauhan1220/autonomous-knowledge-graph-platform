import time
from flask import request


def register_request_logger(app):
    @app.before_request
    def start_timer():
        request.start_time = time.time()

    @app.after_request
    def log_request(response):
        duration_ms = int((time.time() - getattr(request, "start_time", time.time())) * 1000)
        app.logger.info("%s %s %s %sms", request.method, request.path, response.status_code, duration_ms)
        return response
