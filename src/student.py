"""
This module deals with the students and the set of operations that can be
performed on the top of the students.
"""

from model.model_student import Student
from utils import error, create_response


def get_student_info(dict_input_args):
    """
    Gets the student info for the given student id.
    if id is 0 gets all the student info.
    """
    if "id" not in dict_input_args:
        return error(10001, "Missing argument id")
    _id = int(dict_input_args["id"])
    student_info = Student.get_info(_id)
    return create_response(student_info)


def add_student(dict_input_args):
    """
    Adds a new student in the student table
    """
    # todo perform validation on the student data.
    status, _id = Student.add_student(dict_input_args)
    if not status:
        return error(10001, _id)
    else:
        return create_response(_id)
