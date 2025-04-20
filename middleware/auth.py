from functools import wraps
from flask import request, jsonify, current_app
from db import get_db_connection
from datetime import datetime,timedelta
import jwt

def generate_token(User_id,role):
    token =jwt.encode({
                "user":User_id,
                "role":role,
                "exp": datetime.utcnow() + timedelta(hours=1),
            },current_app.config["SECRET_KEY"], algorithm="HS256")
def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers.get('x-access-token')

        elif 'Authorization' in request.headers:
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"message": "Token is missing"}), 401

        try:
            payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            user_id = payload['user']
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401

        return func(user_id, *args, **kwargs)

    return decorated


def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get('Authorization')

            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({'message': 'Token is missing'}), 401

            token = auth_header.split(" ")[1]

            try:
                payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
                user_id = payload['user']
                user_role = payload['role']
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token has expired'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'message': 'Invalid token'}), 401

            if user_role not in required_role:
                return jsonify({'message': f'Unauthorized. Requires {required_role} access.'}), 401

            return f(user_id, *args, **kwargs)

        return decorated_function
    return decorator


def course_enrollment_required():
    def decorator(f):
        @wraps(f)
        def decorated_function(user_id, course_id, *args, **kwargs):
            try:
                cnx = get_db_connection()
                cursor = cnx.cursor()

                cursor.execute("""
                    SELECT * FROM User_Course
                    WHERE user_id = %s AND course_id = %s
                """, (user_id, course_id))

                result = cursor.fetchone()
                cursor.close()
                cnx.close()

                if not result:
                    return jsonify({"message": f"User {user_id} is not enrolled in course {course_id}"}), 403

                return f(user_id, course_id, *args, **kwargs)

            except Exception as err:
                return jsonify({"error": str(err)}), 500

        return decorated_function
    return decorator

