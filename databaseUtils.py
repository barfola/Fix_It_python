import base64

from tableModels import db, Users, Reports
from database import SessionLocal


def create_user_in_db(user_data: dict):
    session = SessionLocal()

    admin_level = user_data["adminLevel"]
    hash_password = user_data["hashPassword"]
    password = user_data["password"]
    user_name = user_data["userName"]
    user_uuid = user_data["uuid"]

    new_user = Users(uuid=user_uuid, username=user_name, password=password, adminLevel=admin_level,
                     hashPassword=hash_password)

    try:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

    except Exception as error:
        session.rollback()
        print(f"Can't add user due to : {error}")

    finally:
        session.close()


def create_user(uuid, username, password, adminLevel):
    session = SessionLocal()
    new_user = Users(uuid=uuid, username=username, password=password, adminLevel=adminLevel)

    try:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

    except Exception as error:
        session.rollback()
        print(f"Can't add user due to : {error}")

    finally:
        session.close()


def create_report(uuid, description, role, location, reportType, user_uuid, image=None):
    session = SessionLocal()

    image_bytes = None

    if image:
        image_bytes = base64.b64decode(image)

    new_report = Reports(uuid=uuid, description=description, role=role, location=location, reportType=reportType,
                         image=image_bytes, userUuid=user_uuid)

    try:
        session.add(new_report)
        session.commit()
        session.refresh(new_report)

    except Exception as error:
        session.rollback()
        print(f"Can't add report due to : {error}")

    finally:
        session.close()


def delete_report(uuid):
    session = SessionLocal()

    try:
        report_to_delete = session.query(Reports).filter_by(uuid=uuid).first()

        if report_to_delete:
            session.delete(report_to_delete)
            session.commit()
            print(f"Report with uuid {uuid} deleted successfully.")
        else:
            print(f"No report found with uuid {uuid}.")

    except Exception as error:
        session.rollback()
        print(f"Can't delete report due to: {error}")

    finally:
        session.close()


def delete_user(uuid):
    session = SessionLocal()

    try:
        user_to_delete = session.query(Users).filter_by(uuid=uuid).first()

        if user_to_delete:
            session.delete(user_to_delete)
            session.commit()
            print(f"User with uuid {uuid} deleted successfully.")
        else:
            print(f"No User found with uuid {uuid}.")

    except Exception as error:
        session.rollback()
        print(f"Can't delete User due to: {error}")

    finally:
        session.close()


def update_report(uuid, description=None, grade=None, location=None, reportType=None, image=None):
    session = SessionLocal()

    try:
        report = session.query(Reports).filter_by(uuid=uuid).first()

        if not report:
            print(f"No report found with uuid {uuid}.")
            return

        if description is not None:
            report.description = description
        if grade is not None:
            report.grade = grade
        if location is not None:
            report.location = location
        if reportType is not None:
            report.reportType = reportType
        if image is not None:
            report.image = image

        session.commit()
        session.refresh(report)
        print(f"Report with uuid {uuid} updated successfully.")

    except Exception as error:
        session.rollback()
        print(f"Can't update report due to: {error}")

    finally:
        session.close()


def update_user(uuid, username=None, password=None, adminLevel=None):
    session = SessionLocal()

    try:
        user = session.query(Users).filter(Users.uuid == uuid).first()
        if not user:
            print("User not found.")
            return

        if username is not None:
            user.username = username
        if password is not None:
            user.password = password
        if adminLevel is not None:
            user.adminLevel = adminLevel

        session.commit()
        session.refresh(user)
        print("User updated successfully.")

    except Exception as error:
        session.rollback()
        print(f"Can't update user due to: {error}")

    finally:
        session.close()


def get_all_users():
    session = SessionLocal()
    try:
        users = session.query(Users).all()
        return users
    except Exception as error:
        print(f"Can't retrieve users due to: {error}")
        return []
    finally:
        session.close()


def get_all_users_reports():
    session = SessionLocal()
    try:
        reports = session.query(Reports).all()
        return reports
    except Exception as error:
        print(f"Can't retrieve reports due to: {error}")
        return []
    finally:
        session.close()


def is_user_name_valid(username):
    session = SessionLocal()
    try:
        user = session.query(Users).filter(Users.username == username).first()
        if user:
            return False
        return True
    except Exception as error:
        print(f"Error checking username validity: {error}")
        return False
    finally:
        session.close()


def is_user_valid(username, password):
    session = SessionLocal()
    try:
        user = session.query(Users).filter(Users.username == username).first()
        if user and user.password == password:
            return True
        return False
    except Exception as error:
        print(f"Error checking user credentials: {error}")
        return False
    finally:
        session.close()


def get_user_uuid(username):
    session = SessionLocal()
    try:
        user = session.query(Users).filter(Users.username == username).first()
        if user:
            return user.uuid
        else:
            return None
    except Exception as error:
        print(f"Error retrieving UUID: {error}")
        return None
    finally:
        session.close()


def get_user_info(username):
    session = SessionLocal()
    try:
        user = session.query(Users).filter(Users.username == username).first()
        if user:
            return user.uuid, user.password, user.username, user.adminLevel, user.hashPassword
        else:
            return None
    except Exception as error:
        print(f"Error retrieving UUID: {error}")
        return None
    finally:
        session.close()


def get_user_info_by_uuid(uuid):
    session = SessionLocal()
    try:
        user = session.query(Users).filter(Users.uuid == uuid).first()
        if user:
            return user.uuid, user.password, user.username, user.adminLevel, user.hashPassword
        else:
            return None
    except Exception as error:
        print(f"Error retrieving user info by UUID: {error}")
        return None
    finally:
        session.close()


def get_reports_by_user_uuid(user_uuid):
    session = SessionLocal()
    try:
        return session.query(Reports).filter_by(userUuid=user_uuid).all()
    except Exception as error:
        print(f"Error getting reports for user {user_uuid}: {error}")
        return []
    finally:
        session.close()



if __name__ == "__main__":
    # print(get_user_uuid("omerbarfy"))
    # print(is_user_valid("omerbarfy","7654321"))
    # print(get_user_info("shaibarfy"))
    #delete_user('b1983e2a-856a-4307-b578-865d96ae62af')
    #print(get_all_users())
    print(get_reports_by_user_uuid("97d1265a-40a6-4f1c-8be4-d96221b4a185"))




