**STUDENT ATTENDANCE MANAGEMENT**

*Dependencies*
- cherrypy
- peewee

To install the dependencies:
'''pip install -r requirements.txt'''

To start the application:
'''python app.py'''

The server runs on the default port of 5000.
To hit any api from the local system after starting the system:
*localhost:5000/api_routes*

*The app is hosted in HEROKU. It can also be accessed
through **https://racetracker.herokuapp.com***


*Basic Authentication is implemented. To access any of the apis in the Authorization
header we will have to pass the username and password. For now the username and
password is admin and admin respectively.*

**List of General APIs available**
1. /api/addstudent?name=foo&reg_no=11234
Adds a new student to the database with the given information.
2. /api/addcourse?name=foo&sr_no=5&start_date=2017-01-01&end_date=2017-06-06&start_time=11:00&end_time=13:00
Adds a new course in the database.
3. /api/registercourse?student_id=1&course_id=1
Registers a student for the given course.
4. /api/recordattendance?student_id=1&course_id=1&status=0&created_date=2017-01-01&created_time=09:00
Takes the attendance of the single student of the given course id. Here status 0 means ABSENT and
status 1 means PRESENT.
5. /api/getstudentinfo?id=1
Returns the student info for the given student id. If the student id is 0 it will return all the student info.
6. /api/getcourseinfo?id=1
Returns the course info for the given course id.
7. /api/getcourseattendancereport?id=1
Returns the attendance report of the given course id.
8. /api/getstudentattendancereport?id=1
Returns the attendance report of the given student id.
9. /api/getregisteredstudents?id=1
Returns the list of the students registered for the given course id.
10. /api/getstudentcourseinfo?id=1
Returns the list of courses registered by the given student id.
