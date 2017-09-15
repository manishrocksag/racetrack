from model_base import BaseModel
import datetime
from peewee import CharField, IntegerField, DateTimeField, PrimaryKeyField, IntegrityError, InternalError, DataError, ForeignKeyField, DateField, TimeField
from model.model_course import Course
from model.model_student import Student


class Attendance(BaseModel):
    id = PrimaryKeyField()
    course_id = ForeignKeyField(Course)
    student_id = ForeignKeyField(Student)
    status = IntegerField()
    created_date = DateField()
    created_time = TimeField()

    @classmethod
    def record_attendance(cls, data):
        try:
            query = BaseModel.db_create_record(data, Attendance)
            return True, query[0].id
        except IntegrityError:
            return False, "Integrity error while inserting data into course table."
        except InternalError:
            return False, "Some internal error while inserting data into course table. "
        except DataError:
            return False, "course data error."

    @classmethod
    def record_attendance_in_bulk(cls, data):
        try:
            query = BaseModel.db_create_multi_record(data, Attendance)
            return True, query
        except IntegrityError:
            return False, "Integrity error while inserting data into course table."
        except InternalError:
            return False, "Some internal error while inserting data into course table. "
        except DataError:
            return False, "course data error."

    @classmethod
    def get_attendance_of_student(cls, student_id):
            db_result = []
            for record in Attendance.select(Attendance.status, \
                Attendance.created_date, Attendance.created_time, \
                Attendance.status, Student.name).dicts() \
                .join(Student, on=Attendance.student_id == Student.id) \
                .join(Course, on=Attendance.course_id == Course.id).where(Attendance.student_id == student_id):

                db_result.append(record)
            return db_result

    @classmethod
    def get_attendance_of_course(cls, course_id):
            db_result = []
            for record in Attendance.select(Attendance.status, \
                Attendance.created_date, Attendance.created_time, \
                Attendance.status, Student.name, Course.name).dicts() \
                .join(Student, on=Attendance.student_id == Student.id) \
                .join(Course, on=Attendance.course_id == Course.id).where(Attendance.course_id == course_id):

                db_result.append(record)
            return db_result
