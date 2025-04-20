from flask import Blueprint, request
from db import get_db_connection
from middleware.auth import course_enrollment_required, role_required, token_required
from utils.helpers import success_response, error_response

forum_bp = Blueprint("forum", __name__)

@forum_bp.route('/create', methods=['POST'])
@role_required("lecturer")
@course_enrollment_required()
def create_forum(user_id, course_id):
    try:
        data = request.json
        forum_id = data["forum_id"]
        title = data["title"]
        info = data["info"]

        cnx = get_db_connection()
        cursor = cnx.cursor()
        cursor.execute("INSERT INTO Forum (forum_id, title, info) VALUES (%s, %s, %s)", (forum_id, title, info))
        cursor.execute("INSERT INTO Course_Forum (forum_id, course_id) VALUES (%s, %s)", (forum_id, course_id))
        cnx.commit()
        return success_response("Forum created")
    except Exception as e:
        return error_response(str(e))

@forum_bp.route('/view', methods=['GET'])
@course_enrollment_required()
def view_forums(user_id, course_id):
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()
        cursor.execute("""SELECT forum_id, title,info
                        FROM vw_course_forums
                        WHERE course_id = %s""", (course_id,))
        forums = cursor.fetchall()
        return success_response([
            {"forum_id": fid, "title": t, "info": i} for fid, t, i in forums
        ])
    except Exception as e:
        return error_response(str(e))



@forum_bp.route('/<int:forum_id>/threads/view', methods=['GET'])
@course_enrollment_required()
def get_threads(user_id, course_id, forum_id):
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()

        cursor.execute("""
            SELECT thread_id, message_info
            FROM vw_forum_threads
            WHERE forum_id = %s
        """, (forum_id,))

        threads = cursor.fetchall()
        result = []
        for thread_id, message_info in threads:
            result.append({
                "thread_id": thread_id,
                "message_info": message_info
            })

        cursor.close()
        cnx.close()
        return success_response(result, 200)
    except Exception as e:
        return error_response({'error': str(e)}, 400)


@forum_bp.route('/<int:forum_id>/threads/create', methods=['POST'])
@course_enrollment_required()
def create_thread(user_id, course_id, forum_id):
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()
        content = request.json

        thread_id = int(content['thread_id'])
        message_info = content['message_info']

        cursor.execute("INSERT INTO Thread (thread_id, message_info) VALUES (%s, %s)",
                       (thread_id, message_info))

        cursor.execute("INSERT INTO Forum_Thread (thread_id, forum_id) VALUES (%s, %s)",
                       (thread_id, forum_id))

        cursor.execute("INSERT INTO ThreadOwner (thread_id, user_id) VALUES (%s, %s)",
                       (thread_id, user_id))

        cnx.commit()
        cursor.close()
        cnx.close()

        return success_response("Thread created successfully", 201)

    except Exception as e:
        return error_response({'error': str(e)}, 400)


@forum_bp.route('/Threads/<int:thread_id>/reply', methods=['POST'])
@token_required
def reply_to_thread(user_id, thread_id):
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()
        content = request.json

        reply_id = int(content['reply_id'])
        message = content['message']
        parent_reply_id = content.get('parent_reply_id')

        cursor.execute("INSERT INTO Reply (reply_id, user_id, message) VALUES (%s, %s, %s)",
                       (reply_id, user_id, message))

        cursor.execute("INSERT INTO Thread_response (reply_id, thread_id) VALUES (%s, %s)",
                       (reply_id, thread_id))

        if parent_reply_id:
            cursor.execute("INSERT INTO Parent_reply (reply_id, parent_reply_id) VALUES (%s, %s)",
                           (reply_id, parent_reply_id))

        cnx.commit()
        cursor.close()
        cnx.close()

        return success_response("Reply added successfully", 201)
    
    except Exception as e:
        return error_response({'error': str(e)}, 400)
