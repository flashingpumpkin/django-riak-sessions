from django.conf import settings
from django.contrib.sessions.backends.base import SessionBase

from riak_sessions import bucket


RIAK_KEY = getattr(settings, 'RIAK_SESSION_KEY', 'session:%(session_key)s')


class SessionStore(SessionBase):
    """
    Riak session store for Django.
    """
    def __init__(self, session_key=None):
        self.bucket = bucket
        self.riak_obj = None
        super(SessionStore, self).__init__(session_key)

    def exists(self, session_key):
        session = self.bucket.get(RIAK_KEY % {'session_key': session_key})
        return session.exists()

    def create(self):
        self.session_key = self._get_new_session_key()
        return self.save(must_create=True)

    def save(self, must_create=False):
        session_data = self._get_session(no_load=must_create)
        encoded_session_data = self.encode(session_data)
        data = { 'data': encoded_session_data, 'expire': self.get_expiry_age() }

        if must_create or self.riak_obj is None:
            self.riak_obj = self.bucket.new(RIAK_KEY % {
                'session_key': self.session_key })

        self.riak_obj.set_data(data)
        self.riak_obj.store()

    def delete(self, session_key=None):
        if session_key is None:
            session_key = self.session_key
        self.bucket.get(RIAK_KEY % {'session_key': session_key}).delete()

    def load(self):
        self.riak_obj = self.bucket.get(RIAK_KEY % dict(session_key=self.session_key))
        if not self.riak_obj.exists():
            self.create()
        data = self.riak_obj.get_data()
        return self.decode(data['data'])
