from django.apps import AppConfig, apps
import requests
from dotenv import load_dotenv
import os
import socket
import atexit
load_dotenv()


class ServiceRegistrarAppConfig(AppConfig):

    name = 'service_registrar'

    registry_url = os.getenv('REGISTRY_URL', 'http://localhost:5000')
    service_name =  service_id = os.getenv('SERVICE_NAME') # maybe add identifier like hostname for id
    service_port = os.getenv('SERVICE_PORT')
    service_host = os.getenv('SERVICE_HOST', socket.gethostname())
    service_address = f'http://{service_host}:{service_port}/api/{service_name}'
    

    def ready(self) -> None:
        
        if not self.service_name or not self.service_port or not self.service_host:
            raise ValueError('SERVICE_NAME, PORT, HOST environment variables are required')
        
        data = {
            'service_name': self.service_name,
            'service_id': self.service_id,
            'service_port': self.service_port,
            'service_host': self.service_host,
            'service_address': self.service_address
        }

        try: 
            healthresp = requests.get(f'{self.registry_url}/health')
            if healthresp.status_code == 200:
                resp = requests.post(f'{self.registry_url}/register', json=data)
                if resp.status_code != 204 and resp.status_code != 201:
                    print(resp.status_code)
                    raise ValueError("lala")
                print('Service registered successfully')
                atexit.register(self.deregister_service)
        except requests.exceptions.ConnectionError:
            print('Registry is not available\nService will not be registered but will be available locally')

        except Exception as e:
            print(f'Failed to register service: ', e)

    def deregister_service(self):
        try:
            resp = requests.post(f'{self.registry_url}/deregister', json={'service_id': self.service_id})
            if resp.status_code == 404:
                pass
            elif resp.status_code != 200:
                raise ValueError()
            
            print('Service deregistered successfully')
        except Exception as e:
            print(f'Failed to deregister service: ', e)



        

        

        
