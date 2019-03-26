from distutils.core import setup

setup(
    name='kbase_cache_client',
    description='Python client for the KBase file cache server',
    version='0.0.1',
    author='rroutsong',
    author_email='info@kbase.us',
    url='https://github.com/rroutsong/kbase_cache_client',
    packages=['kbase_cache_client'],
    license='MIT License',
    long_description=open('README.rst').read(),
    install_requires=[
        'requests>=2.20',
    ],
    python_requires='>3'
)
