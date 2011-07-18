#!/usr/bin/env python
from setuptools import setup,find_packages
import riak_sessions

METADATA = dict(
    name='django-riak-sessions',
    version=riak_sessions.__version__,
    author='Alen Mujezinovic',
    author_email='flashingpumpkin@gmail.com',
    description='Riak session backend for django',
    long_description=open('README.rst').read(),
    url='http://github.com/flashingpumpkin/django-riak-sessions',
    keywords='django riak session backend',
    install_requires=['riak'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Environment :: Web Environment',
        'Topic :: Internet',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    packages=find_packages(),
)

if __name__ == '__main__':
    setup(**METADATA)
    
