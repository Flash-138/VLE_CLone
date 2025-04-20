from flask import Blueprint, request
from db import get_db_connection
from middleware.auth import course_enrollment_required, role_required
from utils.helpers import success_response, error_response

report_bp = Blueprint("report", __name__)


@report_bp.route('/popular-courses', methods=['POST'])
@role_required(["admin", "lecturer"])
def get_popular_courses(user_id):
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor(dictionary=True)

        cursor.execute("SELECT * FROM PopularCourses;")
        data = cursor.fetchall()

        cursor.close()
        cnx.close()
        return success_response(data, 200)

    except Exception as e:
        return error_response({'error': str(e)}, 400)


@report_bp.route('/active-students', methods=['POST'])
@role_required("admin")
def get_active_students(user_id):
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor(dictionary=True)

        cursor.execute("SELECT * FROM ActiveStudents;")
        data = cursor.fetchall()

        cursor.close()
        cnx.close()
        return success_response(data, 200)

    except Exception as e:
        return error_response({'error': str(e)}, 400)


@report_bp.route('/top-lecturers', methods=['POST'])
@role_required("admin")
def get_top_lecturers(user_id):
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor(dictionary=True)

        cursor.execute("SELECT * FROM TopLecturers;")
        data = cursor.fetchall()

        cursor.close()
        cnx.close()
        return success_response(data, 200)

    except Exception as e:
        return error_response({'error': str(e)}, 400)


@report_bp.route('/top-enrolled-courses', methods=['POST'])
@role_required(["admin", "lecturer"])
def get_top_enrolled_courses(user_id):
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor(dictionary=True)

        cursor.execute("SELECT * FROM TopEnrolledCourses;")
        data = cursor.fetchall()

        cursor.close()
        cnx.close()
        return success_response(data, 200)

    except Exception as e:
        return error_response({'error': str(e)}, 400)


@report_bp.route('/top-students-by-grade', methods=['POST'])
@role_required("admin")
def get_top_students_by_grade(user_id):
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor(dictionary=True)

        cursor.execute("SELECT * FROM TopStudentsByGrade;")
        data = cursor.fetchall()

        cursor.close()
        cnx.close()
        return success_response(data, 200)

    except Exception as e:
        return error_response({'error': str(e)}, 400)
