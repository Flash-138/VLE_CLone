from flask import Blueprint, request
from db import get_db_connection
from utils.helpers import success_response, error_response , assign_role
from middleware.auth import generate_token

auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        content = request.json
        user_id = content["user_id"]
        password = content["password"]

        cnx = get_db_connection()
        cursor = cnx.cursor()
        cursor.execute("SELECT user_password, role FROM Logins JOIN User ON Logins.user_id = User.user_id WHERE Logins.user_id = %s", (user_id,))
        record = cursor.fetchone()

        if record and record[0] == password:
            token = generate_token(user_id, record[1])
            return success_response({"message":"User Logged in","token": token})
        return error_response("Invalid credentials", 401)
    except Exception as e:
        return error_response(str(e))


@auth_bp.route('/register_user', methods=['POST'])
def register_user():
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()
        content = request.json

        User_id = int(content['user_id'])
        Password = content["password"]

        Role = assign_role(User_id)
        cursor.execute("INSERT INTO User(user_id,role) VALUES(%s,%s)",(User_id,Role))
        cursor.execute("INSERT INTO Logins(user_id,user_password) VALUES(%s,%s)" , (User_id,Password))
        
        cnx.commit()
        cursor.close()
        cnx.close()
        return success_response(f"User {User_id} was sucessfully created",200)
    except ValueError:
        return error_response(f"Invalid user id", 400)
    except Exception as e:
        return error_response({'error': str(e)}, 400)
    