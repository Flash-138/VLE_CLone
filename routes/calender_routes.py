from flask import Blueprint, request
from db import get_db_connection,DatabaseError
from middleware.auth import role_required,token_required,course_enrollment_required
from utils.helpers import success_response, error_response

calendar_bp = Blueprint("calendar", __name__)

@calendar_bp.route('/view/user', methods=['GET'])
@token_required
def get_calender_Event(user_id):
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()

        content = request.json
        event_date = (content['event_date'])

        cursor.execute("""SELECT event_id, title, event_date
                        FROM vw_user_calendar
                        WHERE user_id = %s
                        AND DATE(event_date) = %s
                        ;""",(user_id,event_date))
        events = cursor.fetchall()
        cnx.commit()
        cursor.close()
        cnx.close()
        

        return success_response(events, 200)
    except Exception as e:
        return error_response({'error': str(e)}, 400)

@calendar_bp.route('/view/course/<string:course_id>', methods=['GET'])
@token_required
@course_enrollment_required()
def get_calender_Event_course(user_id,course_id):
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()

        cursor.execute("""    SELECT title,event_date
                            FROM vw_course_calendar
                            WHERE course_id = %s""",(course_id,))
        
        events = cursor.fetchall()
        cnx.commit()
        cursor.close()
        cnx.close()
        
        return success_response(events, 200)
    except Exception as e:
        return error_response({'error': str(e)}, 400)

@calendar_bp.route('/<string:course_id>/create', methods=['Post'])
@role_required("lecturer")
@course_enrollment_required()
def create_calender_Event_course(user_id,course_id):
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()
        content = request.json
        params = [
            int(content['event_id']),
            content['title'],
            content['event_date'],
            course_id
        ]
        
        cursor.callproc('sp_create_calendar_event', params)
        
        cnx.commit()
        cursor.close()
        cnx.close()
        
        return success_response("Calender Event Created", 200)
    except DatabaseError as err:
        return error_response(err.msg, 400)
    except Exception as e:
        return error_response(str(e))

