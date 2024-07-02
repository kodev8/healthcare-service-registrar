from setuptools import setup, find_packages

setup(
    name='service_registrar',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'Django>=5.0', 
        'requests>=2.26.0',
        'python-dotenv>=0.19.2',
        'djangorestframework>=3.12.4'
    ],
)
