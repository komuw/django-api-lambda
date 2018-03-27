# This sessions package is inspired by: https://github.com/gtaylor/django-dynamodb-sessions
# A few minor modifications have been added and some stuff removed.

import time
import structlog

from django.conf import settings
from django.contrib.sessions.backends.base import SessionBase, CreateError

from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Attr as DynamoConditionAttr
from boto3.session import Session as Boto3Session


TABLE_NAME = getattr(
    settings, 'DYNAMODB_SESSIONS_TABLE_NAME', 'sessions')
HASH_ATTRIB_NAME = getattr(
    settings, 'DYNAMODB_SESSIONS_TABLE_HASH_ATTRIB_NAME', 'session_key')
ALWAYS_CONSISTENT = getattr(
    settings, 'DYNAMODB_SESSIONS_ALWAYS_CONSISTENT', True)

_BOTO_SESSION = getattr(
    settings, 'DYNAMODB_SESSIONS_BOTO_SESSION', False)


if not _BOTO_SESSION:
    AWS_ACCESS_KEY_ID = getattr(
        settings, 'DYNAMODB_SESSIONS_AWS_ACCESS_KEY_ID', False)
    AWS_SECRET_ACCESS_KEY = getattr(
        settings, 'DYNAMODB_SESSIONS_AWS_SECRET_ACCESS_KEY', False)
    AWS_REGION_NAME = getattr(
        settings,
        'DYNAMODB_SESSIONS_AWS_REGION_NAME',
        False)


# We'll find some better way to do this.
_DYNAMODB_CONN = None

logger = structlog.get_logger(__name__)


def dynamodb_connection_factory():
    """
    Since SessionStore is called for every single page view, we'd be
    establishing new connections so frequently that performance would be
    hugely impacted. We'll lazy-load this here on a per-worker basis. Since
    boto3.resource.('dynamodb')objects are state-less (aside from security
    tokens), we're not too concerned about thread safety issues.
    """

    global _DYNAMODB_CONN
    global _BOTO_SESSION
    if not _DYNAMODB_CONN:
        logger.debug("Creating a DynamoDB connection.")
        if not _BOTO_SESSION:
            _BOTO_SESSION = Boto3Session(
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                region_name=AWS_REGION_NAME)
        logger.debug("DynamoDB connected succesfuly.")
        _DYNAMODB_CONN = _BOTO_SESSION.resource('dynamodb')
    return _DYNAMODB_CONN


class SessionStore(SessionBase):
    """
    Implements DynamoDB session store.
    """

    def __init__(self, session_key=None):
        super(SessionStore, self).__init__(session_key)
        self._table = None
        self.logger = structlog.get_logger(
            __name__).bind(session_key=session_key)

    @property
    def table(self):
        if self._table is None:
            self._table = dynamodb_connection_factory().Table(TABLE_NAME)
        return self._table

    def load(self):
        """
        Loads session data from DynamoDB, runs it through the session
        data de-coder (base64->dict), sets ``self.session``.

        :rtype: dict
        :returns: The de-coded session data, as a dict.
        """
        response = self.table.get_item(
            Key={'session_key': self.session_key},
            ConsistentRead=ALWAYS_CONSISTENT)
        self.logger.info('dynamoDB_get_items_response',
                         response=response)
        if 'Item' in response:
            session_data = response['Item']['data']
            return self.decode(session_data)
        else:
            self._session_key = None
            return {}

    def exists(self, session_key):
        """
        Checks to see if a session currently exists in DynamoDB.

        :rtype: bool
        :returns: ``True`` if a session with the given key exists in the DB,
            ``False`` if not.
        """

        response = self.table.get_item(
            Key={'session_key': session_key},
            ConsistentRead=ALWAYS_CONSISTENT)
        if 'Item' in response:
            return True
        else:
            return False

    def create(self):
        """
        Creates a new entry in DynamoDB. This may or may not actually
        have anything in it.
        """

        while True:
            try:
                # Save immediately to ensure we have a unique entry in the
                # database.
                self.save(must_create=True)
            except CreateError:
                continue
            self.modified = True
            self._session_cache = {}
            return

    def save(self, must_create=False):
        """
        Saves the current session data to the database.

        :keyword bool must_create: If ``True``, a ``CreateError`` exception
            will be raised if the saving operation doesn't create a *new* entry
            (as opposed to possibly updating an existing entry).
        :raises: ``CreateError`` if ``must_create`` is ``True`` and a session
            with the current session key already exists.
        """
        # create a session_key if none is provided already
        self._get_or_create_session_key()
        update_kwargs = {
            'Key': {'session_key': self.session_key},
        }
        attribute_names = {'#data': 'data'}
        attribute_values = {
            ':data': self.encode(self._get_session(no_load=must_create))
        }
        set_updates = ['#data = :data']
        if must_create:
            # Set condition to ensure session with same key doesnt exist
            update_kwargs['ConditionExpression'] = \
                DynamoConditionAttr('session_key').not_exists()
            attribute_values[':created'] = int(time.time())
            set_updates.append('created = :created')
        update_kwargs['UpdateExpression'] = 'SET ' + ','.join(set_updates)
        update_kwargs['ExpressionAttributeValues'] = attribute_values
        update_kwargs['ExpressionAttributeNames'] = attribute_names
        try:
            self.logger.info('dynamoDB_table_save',
                             items_to_save=update_kwargs)
            self.table.update_item(**update_kwargs)
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'ConditionalCheckFailedException':
                raise CreateError
            raise

    def delete(self, session_key=None):
        """
        Deletes the current session, or the one specified in ``session_key``.

        :keyword str session_key: Optionally, override the session key
            to delete.
        """

        if session_key is None:
            if self.session_key is None:
                return
            session_key = self.session_key

        self.table.delete_item(Key={'session_key': session_key})
