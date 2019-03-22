.PHONY: test

test:
	echo "Make sure you have a virtual environment activated!."
	pip install -e .
	python tests.py
