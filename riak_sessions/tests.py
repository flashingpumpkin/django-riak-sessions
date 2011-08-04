from django.contrib.sessions.tests import SessionTestsMixin
from django.test import TestCase

from riak_sessions.backends import riak


class RiakSessionTest(SessionTestsMixin, TestCase):
    backend = riak.SessionStore
