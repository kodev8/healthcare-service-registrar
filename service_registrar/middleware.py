from .mixins import ServiceAddressMixin
import requests
from rest_framework.exceptions import NotAuthenticated
import os
from dotenv import load_dotenv
load_dotenv()

class VerifyRequestMiddleware(ServiceAddressMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        self.url = None

    def __call__(self, request):
        try:
            
            if not os.environ.get("ServiceToken") or request.headers.get('ServiceToken') != os.environ.get('ServiceToken'):

                self.get_service_address('authservice')

                token = request.headers.get('Authorization')
                print('TOKEN (1): ',)
                if not token or not token.startswith('Bearer '):
                    raise NotAuthenticated('Invalid token')
                
                _ , token = token.split(' ')
                
                print('TOKEN (2): ', token)
                auth_response = requests.post(f'{self.url}token/verify/', json={'token': token} )
                print('AUTH RESPONSE: ', auth_response.status_code)
                if auth_response.status_code != 200:
                    raise NotAuthenticated('Invalid token')
        
            
        except Exception as exc:
            print(exc)
            return self.response_from_exception(exc)
               
        return self.get_response(request)