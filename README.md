# KBase Cache Server Python Client

This is a python client for the file cache service offered by KBase.

[Documentation for the Caching Service can be found here](https://github.com/kbase/CachingService).

## Installation

Install via pip using the KBase anaconda repository:

```sh
pip install --extra-index-url https://pypi.anaconda.org/kbase/simple \
  kbase_cache_client
```

## Usage

Create the client:

```py
cache_client = KBaseCacheClient('https://appdev.kbase.us/services/')
```

Generate a cache ID:

```py
cacheid = cache_client.generate_cacheid({'test': 'this is a test identifier to id a cache file'})
```

Upload a file to a cache ID:

```py
cache_client.upload_cache(my_file)
```

Download a cached file:

```py
cache_client.download_cache(destination)
```

Delete a cached file:

```py
cache_client.delete_cache()
```

## Development

First, activate a virtual environment with:

```sh
python -m venv env
source env/bin/activate
```

Run tests with **`make test`**.
