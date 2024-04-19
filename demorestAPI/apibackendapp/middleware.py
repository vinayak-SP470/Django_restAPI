from .models import APILog
from django.utils.deprecation import MiddlewareMixin
from django.http import FileResponse
def demo_middleware(get_response):
    def middleware(request):
        response = get_response(request)
        print("before response")
        return response
    print("after response")
    return middleware

class APILogMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        super().__init__(get_response)

    def process_request(self, request):
        request._body = request.body

    def process_response(self, request, response):
        if hasattr(request, '_body'):
            try:
                request_data = request._body.decode('utf-8')
            except UnicodeDecodeError:
                request_data = '[Unable to decode request body]'

            if isinstance(response, FileResponse):
                response_data = '[File response content]'
            else:
                try:
                    response_data = response.content.decode('utf-8')
                except AttributeError:
                    response_data = '[Unable to decode response content]'

            APILog.objects.create(
                endpoint=request.path,
                request_data=request_data,
                response_data=response_data,
                status_code=response.status_code
            )
        return response



# class APILogMiddleware(MiddlewareMixin):
#     def process_response(self, request, response):
#         if hasattr(request, '_logging_enabled') and request._logging_enabled:
#             print("APILogMiddleware")
#             APILog.objects.create(
#                 endpoint=request.path,
#                 request_data=request.body.decode(),
#                 response_data=response.content.decode(),
#                 status_code=response.status_code
#             )
#             print("APILogMiddleware")
#         return response
