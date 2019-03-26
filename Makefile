.PHONY: test build

test:
	echo "Make sure you have a virtual environment activated!."
	pip install -e .
	python tests.py

build:
	echo "Make sure you have a virtual environment activated!."
	pip install -U pip
	pip install -r dev-requirements.txt
	python setup.py sdist
	echo "Publish to anaconda with 'anaconda upload -i -u kbase dist/kbase_cache_client-{version}.tar.gz'"
