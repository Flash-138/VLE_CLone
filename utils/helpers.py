from flask import jsonify, make_response

def success_response(data, code=200):
    # wrap everything under "data"
    return make_response(jsonify({"data": data}), code)

def error_response(message, code=400):
    # wrap errors under "message"
    return make_response(jsonify({"message": message}), code)

def unauthorized_response(message="Unauthorized"):
    return make_response(jsonify({"message": message}), 401)

def assign_role(user_id):
    # Student
    if user_id//10000000 == 62 and 620000000 <= user_id < 630000000:
        return 3
    # Lecturer
    elif user_id//10000 == 100 and 1000000 <= user_id <= 1009999:
        return 2 
    # Admin
    elif user_id//100000 == 999 and 99900000 <= user_id <= 99999999:
        return 1
    else:
        raise ValueError
