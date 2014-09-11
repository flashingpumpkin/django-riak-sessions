import riak
from riak.node import RiakNode
from django.conf import settings
import logging

RIAK_PB_PORT = getattr(settings, 'RIAK_PORT', 8087)
RIAK_HTTP_PORT = getattr(settings, 'RIAK_PORT', 8098)
RIAK_PROTOCOL = getattr(settings, 'RIAK_PROTOCOL', 'pbc')
RIAK_BUCKET = getattr(settings, 'RIAK_BUCKET', 'django-riak-sessions')
RIAK_HOST = getattr(settings, 'RIAK_HOST', '127.0.0.1')
RIAK_NODES = getattr(settings, 'RIAK_NODES', 0)

if not RIAK_NODES:
	RIAK_NODES = []
	riak_node = RiakNode(host=RIAK_HOST, pb_port=RIAK_PB_PORT, http_port=RIAK_HTTP_PORT)
	RIAK_NODES.append(riak_node)
	logging.warning("Using host %s for session caching." % RIAK_HOST)

logging.warning("Using nodes %s for session caching." % RIAK_NODES)
client = riak.RiakClient(protocol=RIAK_PROTOCOL,nodes=RIAK_NODES)
bucket = client.bucket(RIAK_BUCKET)
# TODO This could be ripped out probably, but it's here for now.  Will be chatty.
bucket.set_property('allow_mult',0)
bucket.set_property('backend','mem_be')