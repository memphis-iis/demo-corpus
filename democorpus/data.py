"""demotrack.data

Provide data services to the rest of the application (i.e. the model).

We follow the Amazon DynamoDB terminology and refer to a single record to be
saved as an item. In fact, currently all the code in this module works with
DynamoDB. In a larger application, this would be kept separate
"""

import os
import logging

import boto.exception
import boto.dynamodb2

from boto.dynamodb2.layer1 import DynamoDBConnection
from boto.dynamodb2.table import Table
from boto.dynamodb2.fields import HashKey
from boto.dynamodb2.items import Item
from boto.dynamodb2.exceptions import ResourceNotFoundException, ItemNotFound
from boto.exception import JSONResponseError

logger = logging.getLogger(__name__)


def get_conn():
    """Return a connection to DynamoDB (and handle local/debug possibilities)
    """
    if os.environ.get('DEBUG', None):
        #In DEBUG mode - use the local DynamoDB
        conn = DynamoDBConnection(
            host='localhost',
            port=8000,
            aws_access_key_id='TEST',
            aws_secret_access_key='TEST',
            is_secure=False
        )
    else:
        #Regular old production
        conn = DynamoDBConnection()

    return conn


class InvalidDataObject(Exception):
    """Exception raise when an invalid save operation is attempted
    """
    def __init__(self, errors):
        self.errors = list(errors)
        Exception.__init__("The object was not ready to be saved")


class DefinedTable(object):
    """Abstract base class with some helper functionality to be implemented by
    classes designed to be persisted to the data store. Any property that is
    NOT callable and does NOT begin with an underscore will be included in the
    "item" persisted to the database under the key
    """

    @classmethod
    def get_table_name(cls):
        """Implementors need to tell us the name of the "Table" in the datastore
        """
        raise NotImplementedError("get_table_name is required")

    @classmethod
    def get_key_name(cls):
        """The name of the attribute/property to be used as the key when storing
        in the database.
        """
        raise NotImplementedError("get_table_name is required")
    
    def sort_key(self):
        """Provide a default sort order based on the key for entities of this
        type. Implmenters may override this method if they choose
        """
        return getattr(self, self.get_key_name())

    def errors(self):
        """Implementors can use this function to validate data when save is called:
        individual errors should be yield'ed. The default functionality is to
        yield no errors
        """
        if False:
            yield ''

    def get_item(self):
        """Return a "item" as a dictionary. Every attribute/property that is NOT
        callable and does NOT begin with an underscore will be collected. As a
        result, it's important to make sure that you don't have properties that
        return objects or other "not simple" values.
        """
        key_name = self.get_key_name()
        item = {
            key_name: getattr(self, key_name)
        }

        for prop in dir(self):
            if prop.startswith('_') or prop == key_name:
                continue

            val = getattr(self, prop)
            if not callable(val):
                item[prop] = val

        return item

    def set_from_item(self, item):
        """Given an item (presumably created by calling get_item), set all
        attributes matching the current object
        """
        for key,val in item.items():
            setattr(self, key, val)

    @classmethod
    def ensure_table(cls):
        """Ensure that the table is properly created in the data store
        """
        exists = True
        conn = get_conn()
        table_name = cls.get_table_name()
        try:
            descrip = conn.describe_table(table_name)
        except ResourceNotFoundException:
            logger.debug("Resource not found - Could not find table %s" % table_name)
            exists = False
        except JSONResponseError:
            logger.debug("JSON Response error - ASSUMING could not find table %s" % table_name)
            exists = False

        if not exists:
            key_name = cls.get_key_name()
            logger.debug("Creating table %s with key %s" % (table_name, key_name))
            table = Table.create(
                table_name,
                connection = get_conn(),
                schema=[HashKey(key_name)]
            )

    @classmethod
    def get_class_table(cls):
        """Return a DynamoDB table object for the given DefinedTable instance
        """
        return Table(cls.get_table_name(),
            connection = get_conn(),
            schema = [HashKey(cls.get_key_name())]
        )

    def save(self):
        """Save the results of get_item in the table get_table_name() under the
        key identified by the field name get_key_name(). Note that we unconditionally
        overwrite the data and ignore the possibility someone else has written data
        for this subject.
        """
        all_errors = list(self.errors())
        if all_errors:
            raise InvalidDataObject(errors)

        table = self.get_class_table()
        data = self.get_item()
        logger.debug("SAVING with key %s data %s" % (self.get_key_name(), repr(data)))
        item = Item(table, data=data)
        item.save(overwrite=True)

    @classmethod
    def find_all(cls):
        """Return all items (records) in the table get_table_name() in a list
        """
        final_results = []
        table = cls.get_class_table()
        for db_result in table.scan():
            obj = cls()
            obj.set_from_item(db_result)
            final_results.append(obj)
        
        final_results.sort(key=cls.sort_key)
        
        return final_results

    @classmethod
    def find(cls, key_value):
        """Return a single item (records) in the table get_table_name() matching
        the attribute with get_key_name()
        """
        try:
            db_result = cls.get_class_table().lookup(key_value)
        except ItemNotFound:
            db_result = None #according to docs, this shouldn't be required, but it IS

        if not db_result:
            return None

        obj = cls()
        obj.set_from_item(db_result)
        return obj

    def delete(self):
        """Delete the current record matching the attribute with get_key_name()
        in the table get_table_name()
        """
        table = self.get_class_table()
        item = Item(table, data=self.get_item())
        return item.delete()
