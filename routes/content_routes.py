import io
from flask import send_file, url_for, Blueprint, request
import mimetypes
from db import get_db_connection,DatabaseError
from middleware.auth import role_required, course_enrollment_required, token_required
from utils.helpers import success_response, error_response
from datetime import datetime

content_bp = Blueprint("content", __name__)


@content_bp.route('/add', methods=['POST'])
@role_required("lecturer")
@course_enrollment_required()
def add_content(user_id, course_id):
    try:
        content_id   = int(request.form['content_id'])
        content_name = request.form['content_name']
        content_type = request.form['content_type']
        section_id   = int(request.form['section_id'])

        uploaded = request.files.get('document')
        if not uploaded:
            return error_response("Missing file under key 'document'", 400)
        content_data = uploaded.read()

        params = [
            content_id,
            content_name,
            content_type,
            content_data,
            section_id,
            course_id
        ]

        cnx = get_db_connection()
        cursor = cnx.cursor()

        cursor.callproc('sp_add_content', params)
        cnx.commit()
        return success_response("Content added", 200)

    except DatabaseError as err:
        return error_response(err.msg, 400)
    except KeyError as e:
        return error_response(f"Missing form field: {e.args[0]}", 400)
    except Exception as e:
        return error_response(str(e), 500)


@content_bp.route('/add_text', methods=['POST'])
@role_required("lecturer")
@course_enrollment_required()
def add_content_text(user_id, course_id):
    try:
        payload = request.get_json(force=True)
        content_id   = int(payload['content_id'])
        content_name = payload['content_name']
        content_type = payload['content_type']
        content_text = payload['content_text']
        section_id   = int(payload['section_id'])
        blob = content_text.encode('utf-8')

        cnx    = get_db_connection()
        cursor = cnx.cursor()

        cursor.execute("""
            INSERT INTO Content
              (content_id, contentName, content_type, content_data)
            VALUES
              (%s, %s, %s, %s)
        """, (content_id, content_name, content_type, blob))

        cursor.execute("""
            INSERT INTO SectionContent
              (content_id, section_id)
            VALUES
              (%s, %s)
        """, (content_id, section_id))

        cnx.commit()
        return success_response("Content added", 201)

    except KeyError as e:
        return error_response(f"Missing JSON field: {e.args[0]}", 400)
    except DatabaseError as err:
        return error_response(err.msg, 400)
    except Exception as e:
        return error_response(str(e), 500)


@content_bp.route('/view', methods=['GET'])
@token_required
@course_enrollment_required()
def view_course_content(user_id, course_id):
#application/pdf is content type
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()
        cursor.execute("""
            SELECT
              section_id,
              section_name,
              content_id,
              contentName,
              content_type
            FROM vw_course_content
            WHERE course_id = %s
        """, (course_id,))
        rows = cursor.fetchall()
        cursor.close()
        cnx.close()

        if not rows:
            return success_response([], 200)

        content_map = {}
        for section_id, section_name, content_id, content_name, content_type in rows:
            if section_id not in content_map:
                content_map[section_id] = {
                    "section_name": section_name,
                    "contents": []
                }

            download_url = url_for(
                'content.download_content',
                course_id=course_id,
                content_id=content_id,
                _external=True
            )

            content_map[section_id]["contents"].append({
                "content_id":   content_id,
                "content_name": content_name,
                "content_type": content_type,
                "download_url": download_url
            })

        response = [
            {"section_id": sid, **data}
            for sid, data in content_map.items()
        ]
        return success_response(response, 200)

    except Exception as e:
        return error_response(str(e), 400)


@content_bp.route('/download/<int:content_id>', methods=['GET'])
@role_required(["student","lecturer"])
@course_enrollment_required()
def download_content(user_id, course_id, content_id):
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()
        cursor.execute("""
            SELECT contentName, content_type, content_data
            FROM Content c
            JOIN SectionContent sc ON c.content_id = sc.content_id
            JOIN SectionCourse sc2  ON sc.section_id = sc2.section_id
            WHERE c.content_id = %s
              AND sc2.course_id  = %s
        """, (content_id, course_id))
        row = cursor.fetchone()
        cursor.close()
        cnx.close()

        if not row:
            return error_response("Content not found or unauthorized", 404)

        filename, mimetype, blob = row
        if not isinstance(blob, (bytes, bytearray)):
            raise ValueError("Stored content is not binary data")


        return send_file(
            io.BytesIO(blob),
            as_attachment=True,
            download_name=filename,       
            mimetype=mimetype
        )
        
    except DatabaseError as err:
        return error_response(err.msg, 400)
    except Exception as e:
        return error_response(str(e), 500)

@content_bp.route('/Assignment/add', methods=['POST'])
@role_required("lecturer")
@course_enrollment_required()
def create_assignment(user_id, course_id):
    try:
        aid   = int(request.form['assignment_id'])
        title = request.form['title']
        info  = request.form['info']
        date  = request.form['due_date']

        up = request.files.get('document')
        if not up:
            return error_response("Missing file under key 'document'", 400)
        blob = up.read()

        cnx    = get_db_connection()
        cursor = cnx.cursor()
        cursor.callproc('sp_add_assignment', [
            aid, title, info, date, blob, course_id
        ])
        cnx.commit()
        cursor.close()
        cnx.close()

        return success_response("Assignment created", 201)

    except KeyError as e:
        return error_response(f"Missing form field: {e.args[0]}", 400)
    except DatabaseError as err:
        return error_response(err.msg, 400)
    except Exception as e:
        return error_response(str(e), 500)
    

@content_bp.route('/Assignment/submit', methods=['POST'])
@role_required("student")
@course_enrollment_required()
def submit_assignment(user_id, course_id):
    try:

        submission_id   = int(request.form['submission_id'])
        assignment_id = request.form['assignment_id']
        submit_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S'),

        uploaded = request.files.get('document')
        if not uploaded:
            return error_response("Missing file under key 'document'", 400)
        content_data = uploaded.read()

        params = [
            submission_id,
            assignment_id,
            content_data,
            user_id
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
    

@content_bp.route('/assignment/<int:assignment_id>/download', methods=['GET'])
@role_required(["lecturer", "student"])
@course_enrollment_required()
def download_assignment(user_id, course_id, assignment_id):
    try:
        cnx = get_db_connection()
        cur = cnx.cursor()
        cur.execute("""
            SELECT a.title, a.document
            FROM Assignment a
            JOIN Course_Assignment ca 
              ON a.assignment_id = ca.assignment_id
            WHERE a.assignment_id = %s
              AND ca.course_id     = %s
        """, (assignment_id, course_id))
        row = cur.fetchone()
        cur.close()
        cnx.close()

        if not row:
            return error_response("Assignment not found or unauthorized", 404)

        title, blob = row
        mime, _ = mimetypes.guess_type(title)
        mime = mime or 'application/octet-stream'

        return send_file(
            io.BytesIO(blob),
            as_attachment=True,
            download_name=title,
            mimetype=mime
        )

    except DatabaseError as err:
        return error_response(err.msg, 400)
    except Exception as e:
        return error_response("Internal server error", 500)



@content_bp.route('/submission/<int:submission_id>/download', methods=['GET'])
@role_required(["lecturer", "student"])
@course_enrollment_required()
def download_submission(user_id, course_id, submission_id):
    try:
        cnx = get_db_connection()
        cur = cnx.cursor()
        cur.execute("""
            SELECT s.document, ss.user_id
            FROM Submission s
            JOIN StudentSubmission ss 
              ON s.submission_id = ss.submission_id
            JOIN Course_Assignment ca 
              ON ca.assignment_id = ss.submission_id  -- if you linked them; otherwise drop this JOIN
            WHERE s.submission_id = %s
              AND ca.course_id     = %s
        """, (submission_id, course_id))
        row = cur.fetchone()
        cur.close()
        cnx.close()

        if not row:
            return error_response("Submission not found or unauthorized", 404)

        blob, owner_id = row

        filename = f"submission_{submission_id}"
        mime = 'application/octet-stream'

        return send_file(
            io.BytesIO(blob),
            as_attachment=True,
            download_name=filename,
            mimetype=mime
        )

    except DatabaseError as err:
        return error_response(err.msg, 400)
    except Exception as e:
        return error_response("Internal server error", 500)