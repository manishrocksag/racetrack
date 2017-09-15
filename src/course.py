"""
This module defines the core operations to be perfomred on the courses
taken by different students.
"""

from model.model_course import Course, CourseMapping
from utils import error, create_response


def get_course_info(dict_input_args):
    """
        Takes the course name or code or id and returns the information
        pertaining to the given course.
        if id is 0 gets all the course info.
    """

    if "id" not in dict_input_args:
        return error(10001, "Missing argument id")
    _id = int(dict_input_args["id"])
    student_info = Course.get_info(_id)
    return create_response(student_info)


def add_course(dict_input_args):
    """
        Registers a new course in the database.
    """
    # todo perform validation on the student data.
    status, _id = Course.add_course(dict_input_args)
    if not status:
        return error(10001, _id)
    else:
        return create_response(_id)


def get_registered_students(dict_input_args):
    """
        Get the student registered for the given course.
    """
    if "id" not in dict_input_args:
        return error(10001, "Missing argument id")
    _id = dict_input_args["id"]
    student_info = CourseMapping.get_course_info(_id)
    return create_response(student_info)


def get_student_course_info(dict_input_args):
    """
        Get the student registered for the given course.
    """
    if "id" not in dict_input_args:
        return error(10001, "Missing argument id")
    _id = dict_input_args["id"]
    student_info = CourseMapping.get_registered_student_info(_id)
    return create_response(student_info)


def register_student(dict_input_args):
    # todo perform validation on the student data.
    status, _id = CourseMapping.add(dict_input_args)
    if not status:
        return error(10001, _id)
    else:
        return create_response(_id)
