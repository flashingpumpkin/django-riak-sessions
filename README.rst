Django Riak Sessions
====================

Installation
------------

::

    pip install django-riak-sessions

Configuration
-------------


-  Add ``riak_sessions`` to your installed apps
-  Add the session engine to your settings:

   ::

       SESSION_ENGINE = 'riak_sessions.backends.riak'


Optional Configuration
----------------------

There are a couple of optional configuration values. The default
values are as follows:

::

    import riak
    RIAK_PORT = 8087
    RIAK_HOST = '127.0.0.1'
    RIAK_TRANSPORT_CLASS = riak.RiakPbcTransport
    RIAK_BUCKET = 'django-riak-sessions'
    RIAK_SESSION_KEY = 'session:%(session_key)s'


