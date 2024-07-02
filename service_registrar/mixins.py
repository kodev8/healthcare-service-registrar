import requests
from dotenv import load_dotenv
from rest_framework.exceptions import APIException, NotFound
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
import os
load_dotenv()

class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'

class ServiceAddressMixin:
    code = None
    url = None
    def get_service_address(self, service_name: str) -> str:
        """
        Get the address of a service from the registry
        """
        registry_url = os.getenv('SERVICE_REGISTRY_URL', 'http://localhost:5000')
        try:
            healthresp = requests.get(f'{registry_url}/health')
            self.code = healthresp.status_code
            healthresp.raise_for_status()

            resp = requests.get(f'{registry_url}/service/{service_name}')
            self.code = resp.status_code
            resp.raise_for_status() 

            self.url = resp.json()['Address']
        
        except requests.exceptions.ConnectionError:
            raise ServiceUnavailable('Service registry is not available')
        
        except Exception:
            if self.code == 404:
                raise NotFound(f"Service: '{service_name}' not found")
            
            raise ServiceUnavailable(f"Service: '{service_name}' is not available")
        
    def response_from_exception(self, exc: Exception) -> dict:
        """
        Create a response from an exception
        """
        resp = Response({'detail': str(exc)}, status=exc.status_code if hasattr(exc, 'status_code') else 500)
        resp.accepted_renderer = JSONRenderer()
        resp.accepted_media_type = 'application/json'
        resp.renderer_context = {}
        return resp
        
        
       