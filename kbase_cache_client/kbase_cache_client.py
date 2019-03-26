import requests
import json
import configparser
import os
from pprint import pprint as pp
from .exceptions import (NoCacheIdentifiers, HTTPRequestError,
                         UnknownRequestError, DownloadDirNotWriteable,
                         CacheNonexistent, AuthorizationTokenNotSet)

config = configparser.ConfigParser()
if os.path.exists('test.cfg'):
    config.read('test.cfg')
    if not config.get('KBASE_CACHE_SERVICE', 'TOKEN', fallback=None):
        if not os.getenv('KBASE_CACHE_TOKEN', None):
            raise IOError('Please set your service token in test.cfg, as:\n'
                          '[KBASE_CACHE_SERVICE]\nTOKEN=<token>.\n'
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
        response = requests.post(endpoint, data=json.dumps(identifiers), headers=headers)
        if not response.ok:
            raise RuntimeError('Cache response error: ' + response.text)
        resp_json = response.json()
        if resp_json.get('error'):
            raise HTTPRequestError(resp_json.json().get('error'))
        else:
            self.cache_id = resp_json['cache_id']
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

        if not os.path.isdir(destination):
            dirpath = os.path.dirname(destination)
            if not os.access(dirpath, os.W_OK):
                raise DownloadDirNotWriteable('Please pass a writeable directory to download a cache file to.')
        else:
            if not os.access(destination, os.W_OK):
                raise DownloadDirNotWriteable('Please pass a writeable directory to download a cache file to.')

        if req_call.status_code == 200:
            print('Downloading cache ' + cache_id + '...\nTo: ' + destination)
            with open(destination, 'wb') as f:
                for blob in req_call.iter_content():
                    f.write(blob)
                f.close()
        elif req_call.status_code == 404:
            print('Response code HTTP 404')
            raise HTTPRequestError('Endpoint url: ' + endpoint + ' does not exist.')
        elif req_call.json().get('error'):
            if req_call.json().get('error') == 'Cache ID not found':
                raise CacheNonexistent('Cache ID is nonexistent')
            else:
                pp(req_call.json().get('error'))
                raise HTTPRequestError('An error with the HTTP request occurred see above error message.')
        else:
            pp(req_call)
            print('Request status code: ' + str(req_call.status_code))
            raise UnknownRequestError('Unable to complete request action')

    def upload_cache(self, cache_id, path=None, string=None):
        headers = {'Authorization': self.service_token}
        endpoint = self.cacheurl + 'cache/' + cache_id
        if path:
            with open(path, 'rb') as f:
                req_call = requests.post(endpoint, files={'file': f}, headers=headers)
        elif string:
            req_call = requests.post(endpoint, files={'file': ('data.txt', str.encode(string))}, headers=headers)
        else:
            raise RuntimeError('Pass in a path or a string of data to upload to the cache')

        if req_call.status_code == 200:
            print('Cache ' + cache_id + ' has been successfully uploaded')
            return True
        elif req_call.json().get('error'):
            pp(req_call.json())
            pp(endpoint)
            raise HTTPRequestError('An error with the HTTP request occurred see above error message.')
        else:
            pp(req_call)
            pp(endpoint)
            print('HTTP Status code: ' + str(req_call.status_code))
            raise UnknownRequestError('Unable to complete request action')

    def delete_cache(self, cache_id):
        headers = {'Authorization': self.service_token}
        endpoint = self.cacheurl + 'cache/' + cache_id
        req_call = requests.delete(endpoint, headers=headers)

        if req_call.status_code == 200:
            print('Cache ' + cache_id + ' has been deleted.')
            return True
        elif req_call.json().get('error'):
            if req_call.json().get('error') == 'Cache ID not found':
                raise CacheNonexistent('Cache with id ' + cache_id + ' does not exist')
            else:
                pp(req_call.json())
                pp(endpoint)
                raise HTTPRequestError('An error with the request occurred see above error message.')
        else:
            pp(req_call)
            pp(endpoint)
            print('HTTP Status code: ' + str(req_call.status_code))
            raise UnknownRequestError('Unable to complete request action')
