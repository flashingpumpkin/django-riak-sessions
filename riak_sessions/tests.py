from django.test import TestCase
from django.contrib.sessions.tests import SessionTestsMixin
from riak_sessions.backends import riak

class RiakSessionTest(SessionTestsMixin, TestCase):
    backend = riak.SessionStore
