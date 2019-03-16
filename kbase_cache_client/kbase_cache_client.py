import requests
import json
import configparser
import os
from pprint import pprint as pp


config = configparser.ConfigParser()
if os.path.exists('test.cfg'):
    config.read('test.cfg')

    if not config['SERVICE']['TOKEN']:
        raise ValueError('Please set your service token in test.cfg, as:\n'
                         '[SERVICE]\nTOKEN=<token>.\n'
                         'Consult KBase Administrators if you are not sure how to generate a token')
else:
    raise FileNotFoundError('Please create test.cfg and set your service token as:\n'
                            '[SERVICE]\nTOKEN=<token>\n'
                            'Consult KBase Administrators if you are not sure how to generate a token')


class NoCacheIdentifiers(Exception):
    pass

class HTTPRequestError(Exception):
    pass

class UnknownRequestError(Exception):
    pass

class KBaseCacheClient:
    def __init__(self, service, cache_id=None):
        self.callback = service
        if not self.callback.endswith('/'):
            self.cacheurl = self.callback + '/cache/v1'
        else:
            self.cacheurl = self.callback + 'cache/v1'
        self.service_token = config['SERVICE']['TOKEN']
        self.cache_id = cache_id

    def generate_cacheid(self, identifiers):
        if not isinstance(identifiers, dict):
            raise NoCacheIdentifiers('Identifiers for cache id must be in dictionary format.')

        headers = {'Content-type': 'application/json', 'Authorization': self.service_token}
        endpoint = self.cacheurl + '/cache_id'

        pp(endpoint)
        req_call = requests.get(endpoint, data=json.dumps(identifiers), headers=headers)
        pp(req_call)

        if req_call.json().get('error'):
            raise HTTPRequestError(req_call.get('error'))
        else:
            return req_call['cache_id']

    def download_cache(self, destination):
        headers = {'Content-type': 'application/json', 'Authorization': self.service_token}
        endpoint = self.cacheurl + self.cache_id
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
            pp(req_call.json().get('error'))
            raise HTTPRequestError('An error with the request occurred see above error message.')
        else:
            pp(req_call)
            raise UnknownRequestError(f'Request status code: {req_call.status_code}\n '
                             f'Unable to complete request action')

    def upload_cache(self, source):
        headers = {'Authorization': self.service_token}
        endpoint = self.cacheurl + self.cache_id
        with open(source, 'rb') as f:
            req_call = requests.post(endpoint, files={'file': f}, headers=headers)

        if req_call.status_code == 200:
            print('Cache ' + self.cache_id + ' has been successfully uploaded')
            return True
        elif req_call.json().get('error'):
            pp(req_call.json().get('error'))
            raise HTTPRequestError('An error with the request occurred see above error message.')
        else:
            pp(req_call)
            raise UnknownRequestError(f'Request status code: {req_call.status_code}\n'
                             f'Unable to complete request action')

    def delete_cache(self):
        headers = {'Authorization': self.service_token}
        endpoint = self.cacheurl + self.cache_id
        req_call = requests.delete(endpoint, headers=headers)

        if req_call.status_code == 200:
            print(f'Cache {self.cache_id} has been deleted.')
            return True
        elif req_call.status_code == 404:
            raise ValueError('Cache with id ' + self.cache_id + ' does not exist')
        elif req_call.json().get('error'):
            pp(req_call.json().get('error'))
            raise HTTPRequestError('An error with the request occurred see above error message.')
        else:
            pp(req_call)
            raise UnknownRequestError(f'Request status code: {req_call.status_code}\n Unable to complete request action')
