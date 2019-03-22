from distutils.core import setup

# TODO add requests to the dependencies here

setup(
    name='kbase_cache_client',
    version='0.0.1',
    packages=['kbase_cache_client'],
    license='MIT License',
    long_description=open('README.md').read(),
    install_requires=[
        'requests>=2.20',
    ]
)
