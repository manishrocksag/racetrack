"""
This module takes the attendance of the student and registers it in the
database. The attendance can also be taken in bulk.
"""

from model.model_attendance import Attendance
from utils import error, create_response


def record_attendance(dict_input_args):
    """
    Adds a new attendance record in Attendance Table.
    """
    # todo perform validation on the student data.
    status, _id = Attendance.record_attendance(dict_input_args)
    if not status:
        return error(10001, _id)
    else:
        return create_response(_id)


def record_attendance_in_bulk(dict_input_args):
    """
    Adds a new attendance record in Attendance Table.
    """
    # todo perform validation on the student data.
    status, _id = Attendance.record_attendance_in_bulk(dict_input_args)
    if not status:
        return error(10001, _id)
    else:
        return create_response(_id)


def get_attendance_report_of_student(dict_input_args):
    if "id" not in dict_input_args:
        return error(10001, "Missing argument id")
    _id = dict_input_args["id"]
    attendance_info = Attendance.get_attendance_of_student(_id)
    return create_response(attendance_info)


def get_attendance_report_of_course(dict_input_args):
    if "id" not in dict_input_args:
        return error(10001, "Missing argument id")
    _id = dict_input_args["id"]
    attendance_info = Attendance.get_attendance_of_course(_id)
    return create_response(attendance_info)
