from models import User, Cow, CowBreed, CowDisease, Disease
from flask import request, jsonify, Blueprint, Response
from db_connect import session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

api = Blueprint("api", __name__)

@api.route('/')
def main():
    return jsonify({"message": "Welcome to the Cow Management System!"})

## Purpose :- After User Singup, User info is stored in the database.
## Expects :- JSON object with oauthID, name, role, email - with same keys
@api.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    oauthID = data.get('oauthID')
    name = data.get('name')
    role = data.get('role')
    email = data.get('email')
    location = data.get('location')

    if not oauthID or not name or not email or not location:
        return jsonify({"error": "Missing required fields"}), 400
    
    if role != "" and role not in User.role_options:
        return jsonify({"error": "Invalid role"}), 400

    if oauthID:
        user = session.query(User).filter(User.oauthID == oauthID).first()
        if user:
            return jsonify({"error": "User already exists"}), 400

    try:
        session.add(User(**data))
        session.commit()
        return jsonify({"message": "User added successfully"}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500

## Purpose :- Get list of All Breeds (for Options in dropdown)
@api.route('/get_breeds', methods=['GET'])
def get_breeds():
    breeds = session.query(CowBreed).all()
    return jsonify([breed.serialize() for breed in breeds])
    
## Purpose :- Add Cows owned by the farmer
## Expects :- JSON object with name, dob, health_status, 
#             milk_production, work, breed_id
#             and owner_id, not all keys are mandoatory
@api.route('/add_cow', methods=['POST'])
def add_cow():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    name = data.get('name')
    dob = data.get('dob')
    health_status = data.get('health_status')
    milk_production = data.get('milk_production')
    work = data.get('work')
    breed_id = data.get('breed_id')
    owner_id = data.get('owner_id')

    if not name or not dob or not health_status or not milk_production or not work or not breed_id:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        session.add(Cow(**data))
        session.commit()
        return jsonify({"message": "Cow added successfully"}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500

## Purpose :- Get list of Cows Breeds (and the number of cows of that breed) 
# owned by the farmer
@api.route('/get_cow_breeds_owned/<int:uid>', methods=['GET'])
def get_cow_breeds_ownded(uid):
    # Get list of breeds of cows the farmer owns
    # Each cow has a breed_id that corresponds to a breed
    # Get all cows with the breed_id
    if not uid:
        return jsonify({"error": "Farmer Uid was not provided"}), 400
    elif not session.query(User).filter(User.oauthID == uid).first():
        return jsonify({"error": "Farmer not found"}), 404
    try:
        breeds = (
            session.query(CowBreed.breed,CowBreed.id,func.count(Cow.id).label('count'))
            .join(Cow, Cow.breed_id == CowBreed.id)
            .filter(Cow.owner_id == uid)
            .group_by(CowBreed.id, CowBreed.breed)
            .all()
        )
        result = [{"breed": breed.breed, "count": breed.count} for breed in breeds]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
## Purpose :- Get list of Cows owned by the farmer in a specific breed
@api.route('/get_cows_by_breed/<int:uid>/<int:breed_id>', methods=['GET'])
def get_cows_by_breed(uid, breed_id):
    if not uid or not breed_id:
        return jsonify({"error": "Farmer Uid or Breed ID was not provided"}), 400
    elif not session.query(User).filter(User.oauthID == uid).first():
        return jsonify({"error": "Farmer not found"}), 404
    elif not session.query(CowBreed).filter(CowBreed.id == breed_id).first():
        return jsonify({"error": "Breed not found"}), 404
    try:
        cows = session.query(Cow).filter(Cow.owner_id == uid, Cow.breed_id == breed_id).all()
        return jsonify([cow.serialize() for cow in cows]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
## Purpose :- Get Detail about a specific Cow
@api.route('/get_cow/<int:cow_id>', methods=['GET'])
def get_cow(cow_id):
    if not cow_id:
        return jsonify({"error": "Cow ID was not provided"}), 400
    cow = session.query(Cow).filter(Cow.id == cow_id).first()
    if not cow:
        return jsonify({"error": "Cow not found"}), 404
    return jsonify(cow.serialize()), 200

## Get Breed Details
@api.route('/get_breed/<int:breed_id>', methods=['GET'])
def get_breed(breed_id):
    if not breed_id:
        return jsonify({"error": "Breed ID was not provided"}), 400
    breed = session.query(CowBreed).filter(CowBreed.id == breed_id).first()
    if not breed:
        return jsonify({"error": "Breed not found"}), 404
    return jsonify(breed.serialize()), 200

## set role for a user
@api.route('/set_role', methods=['POST'])
def set_role():
    data = request.get_json()
    if not data :
        return jsonify({"error": "No data provided"}), 400
    role = data.get('role')
    uid = data.get('uid')
    if not role:
        return jsonify({"error": "Invalid role"}), 400
    if not uid:
        return jsonify({"error": "User ID was not provided"}), 400
    user = session.query(User).filter(User.oauthID == uid).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    user.role = role
    try:
        session.commit()
        return jsonify({"message": "Role updated successfully"}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500


## Retreive Role for give user
@api.route('/get_role/<uid>', methods=['GET'])
def get_role(uid):
    if not uid:
        return jsonify({"error": "User ID was not provided"}), 400
    user = session.query(User).filter(User.oauthID == uid).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"role": user.role}), 200