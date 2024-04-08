from rest_framework.renderers import JSONRenderer
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework import status

class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_data = {
            'success': True,
            'message': 'Get Employees successfully',
            'statusCode': 200,
            'data': data
        }

        # Check if the request is unauthorized
        if renderer_context and renderer_context['response'].status_code == HTTP_401_UNAUTHORIZED:
            response_data['success'] = False
            response_data['message'] = 'Unauthorized'
            response_data['statusCode'] = HTTP_401_UNAUTHORIZED
            response_data['data'] = {
                'detail': 'Authentication credentials were not provided.'
            }

        return super().render(response_data, accepted_media_type, renderer_context)


class ProductJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_data = {
            'success': True,
            'data': data
        }
        if renderer_context:
            status_code = renderer_context['response'].status_code
            if status_code == status.HTTP_200_OK:
                response_data['message'] = 'Products listed successfully'
                response_data['statusCode'] = status.HTTP_200_OK
            elif status_code == status.HTTP_401_UNAUTHORIZED:
                response_data['success'] = False
                response_data['message'] = 'Unauthorized'
                response_data['statusCode'] = status.HTTP_401_UNAUTHORIZED
                response_data['data'] = {
                    'detail': 'Authentication credentials were not provided.'
                }
            elif status_code == status.HTTP_204_NO_CONTENT:
                response_data['message'] = 'Product deleted successfully'
                response_data['statusCode'] = status.HTTP_204_NO_CONTENT
            elif status_code == status.HTTP_201_CREATED:
                response_data['message'] = 'Product created successfully'
                response_data['statusCode'] = status.HTTP_201_CREATED
            elif status_code == status.HTTP_400_BAD_REQUEST:
                response_data['success'] = False
                response_data['message'] = 'Bad request'
                response_data['statusCode'] = status.HTTP_400_BAD_REQUEST
                response_data['data'] = {
                    'detail': 'Invalid input data'
                }

        return super().render(response_data, accepted_media_type, renderer_context)