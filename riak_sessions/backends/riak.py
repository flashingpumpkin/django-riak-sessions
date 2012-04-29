from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.sessions.backends.base import SessionBase, CreateError

from riak_sessions import bucket


RIAK_KEY = getattr(settings, 'RIAK_SESSION_KEY', 'session:%(session_key)s')


class SessionStore(SessionBase):
    """
    Riak session store for Django.
    """
    def __init__(self, session_key=None):
        self.bucket = bucket
        super(SessionStore, self).__init__(session_key)

    def _get_riak_key(self, session_key=None):
        if not session_key:
            session_key = self.session_key
        return RIAK_KEY % dict(session_key=session_key)

    def exists(self, session_key):
        session = self.bucket.get(self._get_riak_key(session_key))
        return session.exists()

    def create(self):
        while True:
            self.session_key = self._get_new_session_key()
            try:
                self.save(must_create=True)
            except CreateError:
                # the key wasn't unique, try again
                continue
            self.modified = True
            self._session_cache = {}
            return

    def save(self, must_create=False):
        if must_create:
            current_value = self.bucket.get(self._get_riak_key())
            if current_value.exists():
                return CreateError

        session_data = self._get_session(no_load=must_create)
        encoded_session_data = self.encode(session_data)
        data = {'data': encoded_session_data,
                'expire': int(self.get_expiry_date().strftime("%s"))}

        session = self.bucket.new(self._get_riak_key())
        session.set_data(data)
        session.store()

    def delete(self, session_key=None):
        if session_key is None:
            session_key = self.session_key
        self.bucket.get(self._get_riak_key(session_key)).delete()

    def load(self):
        session = self.bucket.get(self._get_riak_key())

        if session.exists():
            session_data = session.get_data()

            # only return unexpired sessions
            expire_date = datetime.fromtimestamp(session_data['expire'])
            now = datetime.now()
            if (now - expire_date) < timedelta(seconds=settings.SESSION_COOKIE_AGE):
                decoded = self.decode(session_data['data'])
                return decoded

        self.create()
        return {}
