from flask import Blueprint, request
from db import get_db_connection, DatabaseError
from middleware.auth import role_required,token_required,course_enrollment_required
from utils.helpers import success_response, error_response

course_bp = Blueprint("course", __name__)

@course_bp.route('/create', methods=['POST'])
@role_required("admin")
def create_course(user_id):
    try:
        data = request.json
        course_id = data["course_id"]
        course_name = data["course_name"]

        cnx = get_db_connection()
        cursor = cnx.cursor()
        cursor.execute("INSERT INTO Course (course_id, course_name) VALUES (%s, %s)", (course_id, course_name))
        cnx.commit()
        return success_response(f"Course {course_id} created")
    except Exception as e:
        return error_response(str(e))

@course_bp.route('/view', methods=['GET'])
def View_Courses():
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()
        cursor.execute(f"SELECT course_id,course_name from Course")
        courses = cursor.fetchall()
        all_course = []
        for course_id,course_name in courses:
            all_course.append({
                "course_id": course_id,
                "course_name": course_name,
            })

        cursor.close()
        cnx.close()
        return success_response(all_course, 200)
    except Exception as e:
        return error_response({'error': str(e)},400)


@course_bp.route('/view/personal', methods=['GET'])
@token_required
def View_Courses_id(User_id):
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()
        cursor.execute("""SELECT uc.course_id,c.course_name 
                    From User_Course uc
                    Join  Course c ON c.course_id = uc.course_id
                    Where User_id = (%s);""",
                    (User_id,))
        courses = cursor.fetchall()
        if len(courses) == 0:
            raise ValueError
        
        user_courses = []
        for course_id,course_name in courses:
            user_courses.append({
                "course_id": course_id,
                "course_name": course_name,
            })

        cursor.close()
        cnx.close()
        return success_response(user_courses, 200)
    except ValueError:
        return error_response({'No Courses': 'User assigned to no courses found'}, 410)
    except Exception as e:
        return error_response({'error': str(e)})



@course_bp.route('<string:course_id>/register', methods=['POST'])
@role_required(["student", "lecturer"])
def register_course(user_id,course_id):
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()

        params = [
            user_id,
            course_id
        ]

        cursor.callproc('sp_register_course', params)

        cnx.commit()

        cursor.close()
        cnx.close()
        
        return success_response(f"User {user_id} was added to course", 200)
    
    except DatabaseError as err:
        return error_response(err.msg, 400)
    except Exception as e:
        return error_response(str(e), 500)


@course_bp.route('<string:course_id>/members', methods=['GET'])
@token_required
@course_enrollment_required()
def View_user_courses(User_id,Course_id):
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()
        cursor.execute("""SELECT uc.user_id,u.role
                    From user_course uc
                    Join  user u ON u.user_id = uc.user_id
                    Where Course_id = (%s);""",
                    (Course_id,))
        Members = cursor.fetchall()
        if len(Members) == 0:
            raise ValueError

        course_members = []

        for user_id,role in Members:
            course_members.append({
                "user_id": user_id,
                "role": role,
            })

        cursor.close()
        cnx.close()
        return success_response(course_members, 200)
    except ValueError:
        return error_response({'No Members': 'No members assigned to course found'}, 410)
    except:
        return error_response({'error': 'An error has occured'}, 400)
