from model_base import BaseModel
import datetime
from peewee import CharField, IntegerField, DateTimeField, PrimaryKeyField, IntegrityError, InternalError, DataError, ForeignKeyField, DateField, TimeField
from model.model_student import Student

class Course(BaseModel):
    id = PrimaryKeyField()
    name = CharField()
    sr_no = CharField()
    start_date = DateField()
    end_date = DateField()
    start_time = TimeField()
    end_time = TimeField()
    created_date = DateTimeField(default=datetime.datetime.now())
    modified_date = DateTimeField(default=datetime.datetime.now())

    @classmethod
    def add_course(cls, data):
        try:
            query = BaseModel.db_create_record(data, Course)
            return True, query[0].id
        except IntegrityError:
            return False, "Integrity error while inserting data into course table."
        except InternalError:
            return False, "Some internal error while inserting data into course table. "
        except DataError:
            return False, "course data error."

    @classmethod
    def get_info(cls, course_id):
            db_result = []
            for record in Course.select().dicts().where(Course.id == course_id):
                db_result.append(record)
            return db_result

class CourseMapping(BaseModel):
    id = PrimaryKeyField()
    student_id = ForeignKeyField(Student)
    course_id = ForeignKeyField(Course)

    @classmethod
    def add(cls, data):
        try:
            query = BaseModel.db_create_record(data, CourseMapping)
            return True, query[0].id
        except IntegrityError:
            return False, "Integrity error while inserting data into course mapping table."
        except InternalError:
            return False, "Some internal error while inserting data into course mapping table. "
        except DataError:
            return False, "course mapping data error."

    @classmethod
    def get_course_info(cls, course_id):
            db_result = []
            for record in CourseMapping.select(Student.name.alias('student_name'), Course.name.alias('course_name'), Course.start_date, Course.end_date) \
                .dicts().join(Student, on=Student.id == CourseMapping.student_id) \
                .join(Course, on=Course.id == CourseMapping.course_id)\
                .where(CourseMapping.course_id == course_id):

                db_result.append(record)
            return db_result

    @classmethod
    def get_registered_student_info(cls, student_id):
            db_result = []
            for record in CourseMapping.select(Student.name.alias('student_name'), Course.name.alias('course_name'), Course.start_date, Course.end_date) \
                .dicts().join(Student, on=Student.id == CourseMapping.student_id) \
                .join(Course, on=Course.id == CourseMapping.course_id) \
                .where(CourseMapping.student_id == student_id):

                db_result.append(record)
            return db_result
