from models import User, Cow, CowBreed, CowDisease
from flask import request, jsonify, Blueprint, Response
from db_connect import session
from sqlalchemy.orm import sessionmaker

api = Blueprint("api", __name__)

@api.route('/')
def main():
    return jsonify({"message": "Welcome to the Cow Management System!"})

# Post: Receive role info with uid, firebase name, and other user info.
@api.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    oauthID = data.get('oauthID')
    name = data.get('name')
    role = data.get('role')
    email = data.get('email')

    if not oauthID or not name or not role or not email:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        session.add(User(**data))
        session.commit()
        return jsonify({"message": "User added successfully"}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
