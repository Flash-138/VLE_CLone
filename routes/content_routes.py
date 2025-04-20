from flask import Blueprint, request
from db import get_db_connection
from middleware.auth import role_required, course_enrollment_required
from utils.helpers import success_response, error_response
from datetime import datetime

content_bp = Blueprint("content", __name__)


@content_bp.route('/add', methods=['POST'])
@role_required("lecturer")
@course_enrollment_required()
def add_content(user_id, course_id):
    try:
        data = request.json
        content_id = data["content_id"]
        content_name = data["content_name"]
        content_type = data["content_type"]
        content_data = data["content_data"]
        section_id = data["section_id"]

        cnx = get_db_connection()
        cursor = cnx.cursor()

        cursor.execute("SELECT * FROM SectionCourse WHERE section_id = %s AND course_id = %s", (section_id, course_id))
        if not cursor.fetchone():
            return error_response("Section not part of course", 400)

        cursor.execute("INSERT INTO Content (content_id, contentName, content_type, content_data_url) VALUES (%s, %s, %s, %s)", 
                       (content_id, content_name, content_type, content_data))
        cursor.execute("INSERT INTO SectionContent (content_id, section_id) VALUES (%s, %s)", (content_id, section_id))
        cnx.commit()
        return success_response("Content added")
    except Exception as e:
        return error_response(str(e))

@content_bp.route('/view', methods=['GET'])
@course_enrollment_required()
def view_course_content(user_id, course_id):
    try:
        cnx =  get_db_connection()
        cursor = cnx.cursor()

        cursor.execute("""
            SELECT section_id, section_name, content_id, contentName, content_type, content_data_url
            FROM vw_course_content
            WHERE course_id = %s
        """, (course_id,))

        results = cursor.fetchall()

        if not results:
            return success_response({'message': 'No content found for this course.'}, 404)


        content_map = {}
        for section_id, section_name, content_id, content_name, content_type, content_data in results:
            if section_id not in content_map:
                content_map[section_id] = {
                    "section_name": section_name,
                    "contents": []
                }
            content_map[section_id]["contents"].append({
                "content_id": content_id,
                "content_name": content_name,
                "content_type": content_type,
                "content_data": content_data
            })

        response = [{"section_id": sid, **data} for sid, data in content_map.items()]

        cursor.close()
        cnx.close()
        return success_response(response, 200)

    except Exception as e:
        return error_response({'error': str(e)}, 400)


@content_bp.route('/Assignment/submit', methods=['POST'])
@role_required("student")
@course_enrollment_required()
def submit_assignment(user_id, course_id):
    try:
        cnx =  get_db_connection()
        cursor = cnx.cursor()
        content = request.json

        submission_id = int(content['submission_id'])
        assignment_id = int(content['assignment_id'])
        submission_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        document = request.files['document']

        cursor.execute("SELECT * FROM Course_Assignment WHERE course_id = %s AND assignment_id = %s", (course_id, assignment_id))
        if not cursor.fetchone():
            return error_response("Assignment not associated with this course", 400)

        cursor.execute("INSERT INTO Submission (submission_id, submission_date, document) VALUES (%s, %s, %s)",
                       (submission_id, submission_date, document))
        cursor.execute("INSERT INTO StudentSubmission (submission_id, user_id) VALUES (%s, %s)",
                       (submission_id, user_id))

        cnx.commit()
        cursor.close()
        cnx.close()

        return success_response("Assignment submitted successfully", 201)

    except Exception as e:
        return error_response({'error': str(e)}, 400)


@content_bp.route('/Assignment/grade', methods=['POST'])
@role_required("lecturer")
@course_enrollment_required()
def grade_assignment(user_id, course_id):
    try:
        cnx =  get_db_connection()
        cursor = cnx.cursor()
        content = request.json

        assignment_id = int(content['assignment_id'])
        submission_id = int(content['submission_id'])
        grade = int(content['grade'])

        cursor.execute("SELECT * FROM Submission WHERE submission_id = %s", (submission_id,))
        if not cursor.fetchone():
            return error_response("Submission does not exist", 400)

        cursor.execute("REPLACE INTO Grade (assignment_id, submission_id, grade) VALUES (%s, %s, %s)",
                       (assignment_id, submission_id, grade))

        cnx.commit()
        cursor.close()
        cnx.close()

        return success_response("Grade submitted successfully", 200)

    except Exception as e:
        return error_response({'error': str(e)}, 400)
