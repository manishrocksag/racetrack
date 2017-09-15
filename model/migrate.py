import json
import base64
import datetime
import settings
import os

from model.model_base import db
from model.model_student import Student
from model.model_attendance import Attendance
from model.model_course import Course, CourseMapping
from model.model_user import User


def migrate():
    json_file = open(os.path.join('data', 'config.json'), "r")
    data = json.load(json_file)
    json_file.close()

    # Here database_migration is the key for the db engine present in config.json file

    try:
        database = data["database_test"]["db"]
        username = base64.b64decode(data["database_test"]["user"])
        password = base64.b64decode(data["database_test"]["passwd"])
        host = data["database_test"]["host"]
        port = 3306
    except Exception as ex:
        raise Exception("Incorrect Value for db engine")

    db.init(database)

    with db.transaction():

        if settings.RESET_WITH_DUMMY_DATA:
            if Student.table_exists():
                db.drop_tables([Student])

            if Attendance.table_exists():
                db.drop_tables([Attendance])

            if User.table_exists():
                db.drop_tables([User])

            if CourseMapping.table_exists():
                db.drop_tables([CourseMapping])

            if Course.table_exists():
                db.drop_tables([Course])

        if not Student.table_exists():
            db.create_tables([Student])

        if not Attendance.table_exists():
            db.create_tables([Attendance])

        if not User.table_exists():
            db.create_tables([User])

        if not Course.table_exists():
            db.create_tables([Course])

        if not CourseMapping.table_exists():
            db.create_tables([CourseMapping])

        User.create(username="admin",password="admin")
