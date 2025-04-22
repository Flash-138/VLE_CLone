from flask import Blueprint, request
from db import get_db_connection,DatabaseError
from middleware.auth import course_enrollment_required, role_required, token_required
from utils.helpers import success_response, error_response

forum_bp = Blueprint("forum", __name__)

@forum_bp.route('/create', methods=['POST'])
@role_required("lecturer")
@course_enrollment_required()
def create_forum(user_id, course_id):
    try:
        data = request.json
        params = [data["forum_id"],
                  data["title"],
                  data["info"],
                  course_id]
        
        cnx = get_db_connection()
        cursor = cnx.cursor()

        cursor.callproc('sp_create_forum', params)
        cnx.commit()

        return success_response("Forum created")
    except DatabaseError as err:
        return error_response(err.msg, 400)
    except Exception as e:
        return error_response(str(e))

@forum_bp.route('/view', methods=['GET'])
@token_required
@course_enrollment_required()
def view_forums(user_id, course_id):
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()
        cursor.execute("""SELECT forum_id, forum_title,forum_info
                        FROM vw_course_forums
                        WHERE course_id = %s""", (course_id,))
        forums = cursor.fetchall()
        return success_response([
            {"forum_id": fid, "title": t, "info": i} for fid, t, i in forums
        ])
    except Exception as e:
        return error_response(str(e))



@forum_bp.route('/<int:forum_id>/threads/view', methods=['GET'])
@token_required
@course_enrollment_required()
def get_threads(user_id, course_id, forum_id):
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()

        cursor.execute("""
            SELECT thread_id, thread_message
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
@token_required
@course_enrollment_required()
def create_thread(user_id, course_id, forum_id):
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()
        content = request.json

        params = [
            int(content['thread_id']),
            content['message_info'],
            forum_id,
            user_id
        ]

        cursor.callproc('sp_create_thread', params)

        cnx.commit()
        cursor.close()
        cnx.close()

        return success_response("Thread created successfully", 201)

    except DatabaseError as err:
        return error_response(err.msg, 400)
    except Exception as e:
        return error_response({'error': str(e)}, 400)


@forum_bp.route('/threads/<int:thread_id>/reply', methods=['POST'])
@token_required
@course_enrollment_required()
def reply_to_thread(user_id,course_id ,thread_id):
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
    except DatabaseError as err:
        return error_response(err.msg, 400)
    except Exception as e:
        return error_response(str(e), 500)

@forum_bp.route('/threads/<int:thread_id>/view/replies', methods=['GET'])
@token_required
@course_enrollment_required()
def get_replies(user_id, course_id, thread_id):
    """
    Returns a nested list of replies for the given thread_id.
    Each reply may have a 'replies' list of child replies.
    """
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()

        cursor.execute("""
            SELECT r.reply_id,
                   r.user_id,
                   r.message,
                   pr.parent_reply_id
            FROM Reply r
            JOIN Thread_response tr ON r.reply_id = tr.reply_id
            LEFT JOIN Parent_reply pr ON r.reply_id = pr.reply_id
            WHERE tr.thread_id = %s
            ORDER BY r.reply_id
        """, (thread_id,))
        rows = cursor.fetchall()
        cursor.close()
        cnx.close()


        nodes = {}
        for rid, uid, msg, parent in rows:
            nodes[rid] = {
                "reply_id": rid,
                "user_id": uid,
                "message": msg,
                "replies": []
            }


        root = []
        for rid, uid, msg, parent in rows:
            node = nodes[rid]
            if parent is None:
                root.append(node)
            else:
                # parent must exist
                parent_node = nodes.get(parent)
                if parent_node is not None:
                    parent_node["replies"].append(node)

        return success_response(root, 200)

    except Exception as e:
        return error_response(str(e), 500)