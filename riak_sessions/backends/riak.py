from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.sessions.backends.base import SessionBase, CreateError
from django.contrib.sessions.backends.signed_cookies import SessionStore as SignedCookies

from riak_sessions import bucket
import json
import logging

# TODO Remove
# This is to make sure the logger attaches.
logger = logging.getLogger("django.contrib.sessions.middleware")

RIAK_KEY = getattr(settings, 'RIAK_SESSION_KEY', 'session:%(session_key)s')
# Secondary indexes requires python package riak>=1.4.0 and Riak's ELevelDB backend
RIAK_SESSION_USE_2I = getattr(settings, 'RIAK_SESSION_USE_2I', False)


class SessionStore(SessionBase):
    """
    Riak session store for Django.
    """
    def __init__(self, session_key=None):
        self.bucket = bucket
        super(SessionStore, self).__init__(session_key)

    def _get_riak_key(self, session_key=None):
        if not session_key:
            session_key = self._session_key
        return RIAK_KEY % dict(session_key=session_key)

    def _get_expiry_timestamp(self):
        return int(self.get_expiry_date().strftime("%s"))

    def exists(self, session_key):
        session = self.bucket.get(self._get_riak_key(session_key))
        return session.exists

    def create(self):
        while True:
            logger.info("Creating new session...")
            self._session_key = self._get_new_session_key()
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
            if current_value.exists:
                return CreateError

        session_data = self._get_session(no_load=must_create)
        encoded_session_data = self.encode(session_data)
        data = {'data': encoded_session_data,
                'expire': self._get_expiry_timestamp()}

        session = self.bucket.new(self._get_riak_key())
        # TODO Evaluate performance implications
        session.data = json.dumps(data)

        if RIAK_SESSION_USE_2I:
            session.set_indexes([
                ('expire_int', self._get_expiry_timestamp()),
                ('key_bin', self._get_riak_key())
            ])
        session.store()

    def delete(self, session_key=None):
        if session_key is None:
            session_key = self._session_key
        self.bucket.get(self._get_riak_key(session_key)).delete()

    def load(self):
        session = self.bucket.get(self._get_riak_key())

        if session.exists:
            # TODO Evaluate performance implications
            session_data = json.loads(session.data)

            # only return unexpired sessions
            expire_date = datetime.fromtimestamp(session_data['expire'])
            now = datetime.now()
            if (now - expire_date) < timedelta(seconds=settings.SESSION_COOKIE_AGE):
                decoded = self.decode(session_data['data'])
                return decoded
        logger.info("Fell through, this session does not exist...")
        if self._session_key:
            logger.info("Extracting session from old cookie.")
            tempSession = SignedCookies(self._session_key)
            temp_session_state = tempSession.load()
            self.create()
            data = {'data': self.encode(temp_session_state),
                    'expire': self._get_expiry_timestamp()}

            session = self.bucket.new(self._get_riak_key())
            # TODO Evaluate performance implications
            session.data = json.dumps(data)
            session.store()
            return temp_session_state
        self.create()
        return {}
