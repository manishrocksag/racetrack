"""
    cherrypy server to manage all the apis and web sockets connections.
    It exposes the end point to all the apis.
"""

from src.web_command_handler import WebApiHandler
from src.student import get_student_info, add_student
from src.course import add_course, get_course_info, get_registered_students, \
    get_student_course_info, register_student
from src.attendance import record_attendance, record_attendance_in_bulk, \
    get_attendance_report_of_student, get_attendance_report_of_course
from model.migrate import migrate


class App(WebApiHandler):
    """
    Handles all the /api/ path requests
    """

    def __init__(self, listening_port, listening_ip):
        """
        Initialize the application and bind it to IP address and port number.
        """
        super(App, self).__init__(listening_ip, listening_port, 'index.html')

    def api_addstudent(self, args):
        return add_student(args)

    def api_addcourse(self, args):
        return add_course(args)

    def api_recordattendance(self, args):
        return record_attendance(args)

    def api_recordattendanceinbulk(self, args):
        return record_attendance_in_bulk(args)

    def api_getstudentinfo(self, args):
        return get_student_info(args)

    def api_getcourseinfo(self, args):
        return get_course_info(args)

    def api_getcourseattendancereport(self, args):
        return get_attendance_report_of_course(args)

    def api_getstudentattendancereport(self, args):
        return get_attendance_report_of_student(args)

    def api_registercourse(self, args):
        return register_student(args)

    def api_getregisteredstudents(self, args):
        return get_registered_students(args)

    def api_getstudentcourseinfo(self, args):
        return get_student_course_info(args)


def main():
        app = App(5000, '0.0.0.0')
        migrate()
        app.start()


if __name__ == '__main__':
    main()
