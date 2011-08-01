import riak
from django.conf import settings

RIAK_PORT = getattr(settings, 'RIAK_PORT', 8087)
RIAK_TRANSPORT_CLASS = getattr(settings, 'RIAK_TRANSPORT_CLASS', riak.RiakPbcTransport)
RIAK_BUCKET = getattr(settings, 'RIAK_BUCKET', 'django-riak-sessions')
RIAK_HOST = getattr(settings, 'RIAK_HOST', '127.0.0.1')

client = riak.RiakClient(port = RIAK_PORT, host=RIAK_HOST, transport_class = RIAK_TRANSPORT_CLASS)
bucket = client.bucket(RIAK_BUCKET)
