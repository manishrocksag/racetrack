from __future__ import absolute_import, print_function, unicode_literals
from peewee import Model, MySQLDatabase, InternalError, IntegrityError, DataError, SqliteDatabase
import logging

# initialize the database connection
# MySQL DB to be used in production
# db = MySQLDatabase(None)

db = SqliteDatabase(None)
# get the logger for the pack from global configuration file logging.json
logger = logging.getLogger("root")


# parent class for all model tables
class BaseModel(Model):
    class Meta:
        database = db

    @ staticmethod
    def db_create_record(data, table_name, add_fields=None, remove_fields=None, fn_transform=None,
                         fn_validate=None, get_or_create=True):

        """ Takes a file and creates a data frame from it form the input arguments

                Args:
                    data (dict): The record dict to be inserted in table.
                    table_name (Model): The model instance of the table in which the record is to be inserted
                    add_fields (optional argument) (dict): The additional data to be added to record dict.
                    remove_fields (optional argument) (dict): The data to be removed from record dict.
                    fn_transform (optional argument) (dict): The transformation rules if any for the record.
                    fn_validate (optional argument) (dict): The validation rules if any for the record dict.
                    get_or_create (optional argument) (boolean): If set to True gets the record if already exists
                    otherwise creates it. If set to False creates a new record.

                Returns:
                    Model.tuple : The tuple has two records. First record is the id of the record inserted. Second
                                  record is boolean indicating whether the record is already present or it
                                  is inserted now. True indicates the record is inserted now.

                Raises:
                    IntegrityError: If the record with the provided primary key already exists
                    InternalError: If the record to be inserted does not have have valid fields.

                Examples:
                    >>> create_record([], [])
                    [0, 1, 2, 3]

        """
        # List of fields to be removed from data dictionary
        if remove_fields:
            for item in remove_fields:
                data.pop(item, 0)

        # List of additional fields to be added to data dictionary
        if add_fields:
            data.update(add_fields)

        # Transformation rule or function to be applied to data dictionary
        if fn_transform:
            fn_transform(data)

        # Validation rule to be applied to data dictionary
        if fn_validate:
            fn_validate(data)

        try:
            if get_or_create:
                record = table_name.get_or_create(**data)
            else:
                record = table_name.create(**data)
        except DataError as e:
            raise DataError(e)
        except IntegrityError as e:
            raise IntegrityError(e)
        except InternalError as e:
            raise InternalError(e)
        return record

    @staticmethod
    def db_create_multi_record(data, table_name):

        """ Takes a data and creates multiple records for it in db.

                Args:
                    data (list): The record dict to be inserted in table.
                    table_name (Model): The model instance of the table in which the record is to be inserted

                Returns:
                    Model.tuple : The tuple has two records. First record is the id of the record inserted. Second
                                  record is boolean indicating whether the record is already present or it
                                  is inserted now. True indicates the record is inserted now.

                Raises:
                    IntegrityError: If the record with the provided primary key already exists
                    InternalError: If the record to be inserted does not have have valid fields.

                Examples:
                    >>> db_create_multi_record([], [])
                    [0, 1, 2, 3]

        """

        try:
            with db.atomic():
                record = table_name.insert_many(data).execute()
        except DataError as e:
            raise DataError(e)
        except IntegrityError as e:
            raise InternalError(e)
        except InternalError as e:
            raise InternalError(e)
        return record
