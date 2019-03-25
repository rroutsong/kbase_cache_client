import requests
import json
import configparser
import os
from pprint import pprint as pp
from .exceptions import NoCacheIdentifiers, HTTPRequestError, UnknownRequestError, DownloadDirNotaDir, \
    DownloadDirNotWriteable, CacheNonexistent, AuthorizationTokenNotSet

config = configparser.ConfigParser()
if os.path.exists('test.cfg'):
    config.read('test.cfg')

    if not config.get('KBASE_CACHE_SERVICE', 'TOKEN', fallback=None):
        if not os.getenv('KBASE_CACHE_TOKEN', None):
            raise ValueError('Please set your service token in test.cfg, as:\n'
                             '[KBASE_CACHE_SERVICE]\nTOKEN=<token>.\n'
                             'Or as an environmental variable KBASE_CACHE_TOKEN\n'
                             'Consult KBase Administrators if you are not sure how to generate a token')
else:
    if not os.getenv('KBASE_CACHE_TOKEN', None):
        raise FileNotFoundError('Please create test.cfg and set your service token as:\n'
                                '[KBASE_CACHE_SERVICE]\nTOKEN=<token>\n'
                                'Or as an environmental variable KBASE_CACHE_TOKEN\n'
                                'Consult KBase Administrators if you are not sure how to generate a token')

class KBaseCacheClient:
    def generate_cacheid(self, identifiers):
        if not isinstance(identifiers, dict):
            raise NoCacheIdentifiers('Identifiers for cache id must be in dictionary format.')

        headers = {'Content-type': 'application/json', 'Authorization': self.service_token}

        if not self.callback.endswith('/'):
            endpoint = self.callback + '/cache/v1/cache_id'
        else:
            endpoint = self.callback + 'cache/v1/cache_id'

        req_call = requests.post(endpoint, data=json.dumps(identifiers), headers=headers).json()

        if req_call.get('error'):
            pp(req_call)
            raise HTTPRequestError(req_call.json().get('error'))
        else:
            self.cache_id = req_call['cache_id']
            return self.cache_id

    def __init__(self, service, token=None):
        self.callback = service
        if not self.callback.endswith('/'):
            self.cacheurl = self.callback + '/cache/v1/'
        else:
            self.cacheurl = self.callback + 'cache/v1/'

        if token is None:
            if config.get('KBASE_CACHE_SERVICE', 'TOKEN', fallback=None):
                self.service_token = config.get('KBASE_CACHE_SERVICE', 'TOKEN', fallback=None)
            elif os.getenv('KBASE_CACHE_TOKEN', None):
                self.service_token = os.getenv('KBASE_CACHE_TOKEN', None)
            else:
                raise AuthorizationTokenNotSet('Please set your authorization token on class initialization.')
        else:
            self.service_token = token

    def download_cache(self, cache_id, destination):
        headers = {'Content-type': 'application/json', 'Authorization': self.service_token}
        endpoint = self.cacheurl + 'cache/' + cache_id
        req_call = requests.get(endpoint, headers=headers, stream=True)

        if req_call.status_code == 200:
            print(f'Downloading cache {self.cache_id}...\nTo: {destination}')
            with open(destination, 'wb') as f:
                for blob in req_call.iter_content():
                    f.write(blob)
                f.close()
        elif req_call.status_code == 404:
            raise ValueError(f'Cache with id {self.cache_id} does not exist')
        elif req_call.json().get('error'):
            if req_call.json().get('error') is 'Cache ID not found':
                raise CacheNonexistent('Cache ID is nonexistent')
            else:
                pp(req_call.json().get('error'))
                raise HTTPRequestError('An error with the HTTP request occurred see above error message.')
        else:
            pp(req_call)
            raise UnknownRequestError(f'Request status code: {req_call.status_code}\n '
                             f'Unable to complete request action')

    def upload_cache(self, cache_id, source):
        headers = {'Authorization': self.service_token}
        endpoint = self.cacheurl + 'cache/' + cache_id

        with open(source, 'rb') as f:
            req_call = requests.post(endpoint, files={'file': f}, headers=headers)

        if req_call.status_code is 200:
            print(f'Cache {cache_id} has been successfully uploaded')
            return True
        elif req_call.json().get('error'):
            pp(req_call.json())
            pp(endpoint)
            raise HTTPRequestError('An error with the HTTP request occurred see above error message.')
        else:
            pp(req_call)
            pp(endpoint)
            raise UnknownRequestError(f'Request status code: {req_call.status_code}\n'
                             f'Unable to complete request action')

    def delete_cache(self, cache_id):
        headers = {'Authorization': self.service_token}
        endpoint = self.cacheurl + 'cache/' + cache_id
        req_call = requests.delete(endpoint, headers=headers)

        if req_call.status_code is 200:
            print(f'Cache {cache_id} has been deleted.')
            return True
        elif req_call.json().get('error'):
            if req_call.json().get('error') is 'Cache ID not found':
                raise CacheNonexistent(f'Cache with id {cache_id} does not exist')
            else:
                pp(req_call.json())
                pp(endpoint)
                raise HTTPRequestError('An error with the request occurred see above error message.')
        else:
            pp(req_call)
            pp(endpoint)
            raise UnknownRequestError(f'Request status code: {req_call.status_code}\n Unable to complete request action')
