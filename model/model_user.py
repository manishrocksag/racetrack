from model_base import BaseModel
import datetime
from peewee import CharField, IntegerField, DateTimeField, PrimaryKeyField, IntegrityError, InternalError, DataError,\
    ForeignKeyField, DateField


class User(BaseModel):
    id = PrimaryKeyField()
    username = CharField()
    password = CharField()
    created_date_time = DateTimeField(default=datetime.datetime.now())

    @classmethod
    def get_users():
        user_info = {}
        for record in User.select(User.username, User.password).dicts():
            user_info[record["username"]] = record["password"]
        return user_info
