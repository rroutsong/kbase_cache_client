KBase Cache Server Python Client
--------------------------------

This is a python client for the file cache service offered by KBase.

Documentation for the KBase file cache server can be found here: https://github.com/kbase/CachingService

Installation
============

Install via pip using the KBase anaconda repository:

.. code-block:: bash

    pip install -i https://pypi.anaconda.org/kbase/simple kbase_cache_client

Usage
=====

Create the client:

.. code-block:: python

    cache_client = KBaseCacheClient('https://appdev.kbase.us/services/')

Generate a cache ID:

.. code-block:: python

    cacheid = cache_client.generate_cacheid({'test': 'this is a test identifier to id a cache file'})

Upload a file to a cache ID:

.. code-block:: python

    cache_client.upload_cache(my_file)

Download a cached file:

.. code-block:: python

    cache_client.download_cache(destination)

Delete a cached file:

.. code-block:: python

    cache_client.delete_cache()

Development
===========

First, activate a virtual environment with:

.. code-block:: bash

  python -m venv env
  source env/bin/activate

Run tests with ``make test``

Publishing
==========

To build the pip package, first run ``make build``

Publish the package to anaconda under the kbase org:

.. code-block:: bash

    anaconda upload -i -u kbase dist/kbase_cache_client-{version}.tar.gz
