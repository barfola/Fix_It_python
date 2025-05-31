from flask import Flask, request, jsonify
from tableModels import db, Users, Reports
from datetime import datetime, timedelta
import uuid
from Enums import Location, Role, ReportType
from databaseUtils import *

session_store = {}
SESSION_DURATION_SECONDS = 500

server = Flask(__name__)
fix_it_db_path = r"D:\Cyber\project\db\fixitdb.db"
server.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{fix_it_db_path}'

db.init_app(server)


def is_session_expired(session_id: str) -> bool:
    global session_store
    print(f"The session id is : {session_id}")
    print(f"Session store data : {session_store}")

    login_time = session_store.get(session_id)
    if not login_time:
        return True

    return datetime.now() > login_time + timedelta(seconds=SESSION_DURATION_SECONDS)


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
    if not is_session_expired(session_id):
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
    if not is_session_expired(session_id):
        pass
    sample_data = {
        "reportId": 1,
        "description": "Broken table in classroom",
        "grade": "9th",
        "location": "Room 203"
    }
    return jsonify(sample_data), 200


@server.route('/session_id', methods=['GET'])
def send_session_id():
    session_id = save_user_session()
    data = {
        'session_id': session_id
    }

    return jsonify(data), 200


@server.route("/get_image", methods=["GET"])
def get_image():
    uuid = request.args.get("uuid")
    base64_image = get_report_image_base64(uuid)

    if base64_image:
        return jsonify({"image": base64_image}), 200
    else:
        return jsonify({"error": "Image not found"}), 404


@server.route('/delete_report', methods=['DELETE'])
def delete_report_by_admin():
    uuid = request.args.get("uuid")
    session_id = request.args.get("sessionId")
    user_uuid = request.args.get("userUuid")

    if not is_session_expired(session_id):
        pass

    try:

        delete_report(uuid)

        return jsonify({"message": "Report deleted"}), 200

    except Exception as error:
        return jsonify({"error": str(error)}), 500


@server.route('/get_all_reports', methods=['GET'])
def get_all_reports():
    user_uuid = request.args.get("userUuid").strip()
    session_id = request.args.get("sessionID").strip()

    print(f"Received GET: userUuid={user_uuid}, sessionID={session_id}")

    if not user_uuid or not session_id:
        print("invalid credentials")
        return jsonify({"error": "Missing userUuid or sessionID"}), 400

    if is_session_expired(session_id):
        print("invalid session")
        return jsonify({"error": "Invalid session"}), 401

    session = SessionLocal()

    try:
        all_reports = get_all_users_reports()

        result = []
        for report in all_reports:
            result.append({
                "uuid": report.uuid,
                "description": report.description,
                "role": report.role,  # assuming stored as int
                "location": report.location,
                "reportType": report.reportType,
                "image": None
                #"image": base64.b64encode(report.image).decode() if report.image else None

            })

        return jsonify(result), 200

    except Exception as error:
        print(f"Error retrieving reports: {error}")
        return jsonify({"error": str(error)}), 500

    finally:
        session.close()


@server.route('/get_reports', methods=['GET'])
def get_reports_by_user():
    global session_store

    user_uuid = request.args.get("userUuid").strip()
    session_id = request.args.get("sessionID").strip()

    print(f"Received GET: userUuid={user_uuid}, sessionID={session_id}")

    if not user_uuid or not session_id:
        print("invalid credentials")
        return jsonify({"error": "Missing userUuid or sessionID"}), 400

    print(f"The session is {session_id}")
    print(f"is ok{is_session_expired(session_id)}")

    if is_session_expired(session_id):
        print("invalid session")
        del session_store[session_id]
        return jsonify({"error": "Session expired"}), 401

    session = SessionLocal()

    try:
        user_reports = session.query(Reports).filter_by(userUuid=user_uuid).all()

        result = []
        for report in user_reports:
            result.append({
                "uuid": report.uuid,
                "description": report.description,
                "role": report.role,  # assuming stored as int
                "location": report.location,
                "reportType": report.reportType,
                "image": None  # In this final version of my app I don't need the image(A lot of images causes to : unexpected end of streem)
                # "image": base64.b64encode(report.image).decode() if report.image else None

            })

        return jsonify(result), 200

    except Exception as error:
        print(f"Error retrieving reports: {error}")
        return jsonify({"error": str(error)}), 500

    finally:
        session.close()


@server.route('/problemReport', methods=['POST'])
def receive_report():
    global session_store
    data = request.get_json()
    print(f"The report data is : {data}")

    user_uuid = request.args.get("userUuid").strip()
    session_id = request.args.get("sessionID").strip()

    if not user_uuid or not session_id:
        print("invalid credentials")
        return jsonify({"error": "Missing userUuid or sessionID"}), 400

    if is_session_expired(session_id):
        print("invalid session")
        del session_store[session_id]
        return jsonify({"error": "Invalid session"}), 401

    try:
        uuid = data.get("uuid")
        description = data.get("description")
        role_int = data.get("role")
        location_int = data.get("location")
        report_type_int = data.get("reportType")
        image = data.get("image")

        try:
            role = Role(role_int)
            location = Location(location_int)
            report_type = ReportType(report_type_int)

        except ValueError as e:
            return jsonify({"error": f"Invalid enum value: {e}"}), 400

        print(f"uuid: {uuid}")
        print(f"Description: {description}")
        print(f"Role: {role.name}")
        print(f"Location: {location.name}")
        print(f"Report Type: {report_type.name}")
        print(f"User UUID: {user_uuid}")
        print(f"Session ID: {session_id}")
        print(f"Image: {image}")

        create_report(uuid, description, role.value, location.value, report_type.value, user_uuid, image)

        return jsonify({"message": "Report received"}), 200
    except Exception as error:
        print("Error in /problemReport:", error)
        return jsonify({"error": str(error)}), 500


@server.route('/initialCredentials', methods=['Post'])
def initial_credentials():
    credentials = request.get_json()
    uuid = credentials.get("uuid")
    session_id = credentials.get("sessionId")
    try:
        if not is_session_expired(session_id):
            user_uuid, user_password, user_username, user_admin_level, user_hash_password = get_user_info_by_uuid(uuid)
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
            return jsonify({'message': 'Session expired'}), 401

    except Exception as error:
        print("Error processing user data:", str(error))
        return jsonify({'error': 'Failed to process user data'}), 400


@server.route('/login', methods=['POST'])
def user_login():
    global session_store
    login_data = request.get_json()
    username = login_data.get("userName")
    password = login_data.get("password")
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
            print(response_data)
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
            print("user created in user table")
            return jsonify({'message': 'User received successfully', 'sessionId': session_id}), 200

        else:
            return jsonify({'message': 'Invalid username'}), 401

    except Exception as error:
        print("Error processing user data:", str(error))
        return jsonify({'error': 'Failed to process user data'}), 400


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=5000)
