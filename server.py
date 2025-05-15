from flask import Flask, request, jsonify
from tableModels import db, Users, Reports
from datetime import datetime, timedelta
import uuid
from Enums import Location, Role, ReportType
from databaseUtils import *

session_store = {"1": datetime.now()}
SESSION_DURATION_MINUTES = 80

server = Flask(__name__)
fix_it_db_path = r"D:\Cyber\project\db\fixitdb.db"
server.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{fix_it_db_path}'

db.init_app(server)


def check_user(session_id: str) -> bool:
    login_time = session_store.get(session_id)
    if not login_time:
        return False
    return datetime.now() < login_time + timedelta(minutes=SESSION_DURATION_MINUTES)


def save_user_session() -> str:
    session_id = str(uuid.uuid4())
    session_store[session_id] = datetime.now()
    return session_id


@server.route('/')
def home():
    return 'Flask app connected to existing SQLite DB with Users and Reports tables!'


@server.route('/users')
def list_users():
    users = Users.query.all()
    return '<br>'.join([f'{user.username} (Admin: {user.adminLevel})' for user in users])


@server.route('/reports')
def list_reports():
    reports = Reports.query.all()
    return '<br>'.join([f'{report.description} - {report.grade} - {report.location}' for report in reports])


@server.route('/receive_user', methods=['POST'])
def receive_user():
    data = request.get_json()
    session_id = data.get('sessionId')
    if not check_user(session_id):
        pass
    data = request.get_json()
    # session_id = data.get('sessionId')
    # if not check_user(session_id):
    #     return 'session expired', 401

    print(f"Received user data : {data}")
    return '', 200


@server.route('/get_report', methods=['GET'])
def get_report():
    data = request.get_json()
    session_id = data.get('sessionId')
    if not check_user(session_id):
        pass
    sample_data = {
        "reportId": 1,
        "description": "Broken table in classroom",
        "grade": "9th",
        "location": "Room 203"
    }
    return jsonify(sample_data), 200


@server.route('/receive_report', methods=['POST'])
def receive_report():
    data = request.get_json()
    #session_id = data.get('sessionId')

    # if not check_user(session_id):
    #     print("session is not valid")
    #     return 'session expired', 401

    print(f"Received report data : {data} ")
    print(ReportType[data.get('reportType')])
    return '', 200


@server.route('/delete_report', methods=['POST'])
def delete_report():
    data = request.get_json()
    session_id = data.get('sessionId')
    if not check_user(session_id):
        pass


@server.route('/update_report', methods=['POST'])
def update_report():
    data = request.get_json()
    session_id = data.get('sessionId')
    if not check_user(session_id):
        pass


@server.route('/session_id', methods=['GET'])
def send_session_id():
    session_id = save_user_session()
    data = {
        'session_id': session_id
    }

    return jsonify(data),200


@server.route('/login', methods=['POST'])
def user_login():
    global session_store
    login_data = request.get_json()
    username = login_data.get("userName")
    password = login_data.get("password")
    print(f"login_data:{login_data}")
    try:
        if is_user_valid(username, password):
            session_id = save_user_session()
            user_uuid, user_password, user_username, user_admin_level, user_hash_password = get_user_info(username)
            print(f'the session is : {session_id}')
            print(f"Session store: {session_store}")
            response_data = {'message': 'User logged in successfully',
                             'sessionId': session_id,
                             'uuid': user_uuid,
                             'userName': user_username,
                             'password': user_password,
                             'hashPassword': user_hash_password,
                             'adminLevel': user_admin_level,
                             }
            return jsonify(response_data), 200

        else:
            return jsonify({'message': 'Invalid username or password'}), 401

    except Exception as error:
        print("Error processing user data:", str(error))
        return jsonify({'error': 'Failed to process user data'}), 400



@server.route('/signin', methods=['POST'])
def user_signin():
    try:
        sign_in_data = request.get_json()
        username = sign_in_data.get("userName")
        print(f"sign_in_data:{sign_in_data}")
        if is_user_name_valid(username):
            session_id = save_user_session()
            print(session_id)
            create_user_in_db(sign_in_data)
            return jsonify({'message': 'User received successfully', 'sessionId': session_id}), 200

        else:
            return jsonify({'message': 'Invalid username'}), 401

    except Exception as error:
        print("Error processing user data:", str(error))
        return jsonify({'error': 'Failed to process user data'}), 400





if __name__ == '__main__':
    server.run(host='0.0.0.0', port=5000)
