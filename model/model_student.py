from model_base import BaseModel
import datetime
from peewee import CharField, IntegerField, DateTimeField, PrimaryKeyField, IntegrityError, InternalError, DataError,\
    ForeignKeyField
import settings

class Student(BaseModel):
    id = PrimaryKeyField()
    name = CharField()
    reg_no = CharField()
    created_date = DateTimeField(default=datetime.datetime.now())
    modified_date = DateTimeField(default=datetime.datetime.now())

    @classmethod
    def add_student(cls, data):
        try:
            query = BaseModel.db_create_record(data, Student)
            return True, query[0].id
        except IntegrityError:
            return False, "Integrity error while inserting data into student table."
        except InternalError:
            return False, "Some internal error while inserting data into student table. "
        except DataError:
            return False, "Student data error."

    @classmethod
    def get_info(cls, student_id):
        db_result = []
        if student_id == settings.NULL:
            for record in Student.select().dicts():
                db_result.append(record)
        else:
            for record in Student.select().dicts().where(Student.id == student_id):
                db_result.append(record)
        return db_result
