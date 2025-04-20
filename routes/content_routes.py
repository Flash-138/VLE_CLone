from flask import Blueprint, request
from db import get_db_connection,DatabaseError
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
        params = [
            data["content_id"],
            data["content_name"],
            data["content_type"],
            data["content_data"],    
            data["section_id"],
            course_id
        ]

        cnx = get_db_connection()
        cursor = cnx.cursor()

        cursor.callproc('sp_add_content', params)
        cnx.commit()
        return success_response("Content added", 201)

    except DatabaseError as err:
        return error_response(err.msg, 400)
    except Exception as e:
        return error_response(str(e), 500)

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
        
        content = request.json
        params = [
            int(content['submission_id']),
            int(content['assignment_id']),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
            request.files['document'].read(),
        ]
        
        cnx =  get_db_connection()
        cursor = cnx.cursor()


        cursor.callproc('sp_submit_assignment', params)
        cnx.commit()

        cursor.close()
        cnx.close()

        return success_response("Assignment submitted successfully", 201)

    except DatabaseError as err:
        return error_response(err.msg, 400)
    except Exception as e:
        return error_response(str(e), 500)


@content_bp.route('/Assignment/grade', methods=['POST'])
@role_required("lecturer")
@course_enrollment_required()
def grade_assignment(user_id, course_id):
    try:
        cnx =  get_db_connection()
        cursor = cnx.cursor()
        content = request.json

        params = [
            int(content['assignment_id']),
            int(content['submission_id']),
            int(content['grade'])
        ]

        cursor.callproc('sp_grade_assignment', params)

        cnx.commit()
        cursor.close()
        cnx.close()

        return success_response("Grade submitted successfully", 200)

    except DatabaseError as err:
        return error_response(err.msg, 400)
    except Exception as e:
        return error_response(str(e), 500)