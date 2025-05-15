from flask import Flask, request, jsonify
from tableModels import db, Users, Reports
from datetime import datetime, timedelta
import uuid

session_store = {"1": datetime.now()}
SESSION_DURATION_MINUTES = 30


def check_user(session_id: str) -> bool:
    login_time = session_store.get(session_id)
    if not login_time:
        return False
    return datetime.now() < login_time + timedelta(minutes=SESSION_DURATION_MINUTES)


print(check_user("1"))