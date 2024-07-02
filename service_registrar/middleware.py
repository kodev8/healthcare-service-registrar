from .mixins import ServiceAddressMixin
import requests
from rest_framework.exceptions import NotAuthenticated

class VerifyRequestMiddleware(ServiceAddressMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        self.url = None

    def __call__(self, request):
        try:
            self.get_service_address('auth_service')

            token = request.headers.get('Authorization')
            if not token or not token.startswith('Bearer '):
                raise NotAuthenticated('Invalid token')
            
            _ , token = token.split(' ')

            auth_response = requests.post(f'{self.url}/token/verify/', json={'token': token} )
            
            if auth_response.status_code != 200:
                raise NotAuthenticated('Invalid token')
            
        except Exception as exc:
            return self.response_from_exception(exc)
               
        return self.get_response(request)