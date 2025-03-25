from models import User, Cow, CowBreed, CowDisease, Disease, Notification
from flask import request, jsonify, Blueprint, Response
from db_connect import session
from sqlalchemy.orm import sessionmaker,joinedload
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from math import radians, sin, cos, sqrt, atan2


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
    try:
        # Query only the breed names
        breeds = session.query(CowBreed.breed).all()
        # Extract breed names from the query result
        breed_names = [breed[0] for breed in breeds]
        return jsonify(breed_names), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
## Purpose :- Add Cows owned by the farmer
## Expects :- JSON object with name, dob, health_status, 
#             milk_production, work, breed_id
#             and owner_id, not all keys are mandoatory
@api.route('/add_cow', methods=['POST'])
def add_cow():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Extract required fields
    name = data.get('name')
    breed = data.get('breed')  # Breed name from the frontend
    birth_date = data.get('birthDate')  # Birth date in YYYY-MM-DD format
    oauth_id = data.get('owner_id')  # Owner's oauthID from the frontend
    milk_production = data.get('milk_production')  # Milk production in liters

    # Extract optional fields
    tag_number = data.get('tagNumber', None)
    notes = data.get('notes', None)

    try:
        # Resolve oauthID to user ID
        user = session.query(User).filter(User.oauthID == oauth_id).first()
        if not user:
            return jsonify({"error": f"User with oauthID '{oauth_id}' not found"}), 404
        owner_id = user.id

        # Resolve breed name to breed_id
        breed_obj = session.query(CowBreed).filter(func.lower(CowBreed.breed) == breed.lower()).first()
        if not breed_obj:
            return jsonify({"error": f"Breed '{breed}' not found"}), 404

        # Create a new Cow object
        new_cow = Cow(
            name=name,
            breed_id=breed_obj.id,
            dob=birth_date,
            health_status='Healthy',  # Default health status
            milk_production=milk_production,
            owner_id=owner_id,
            work=None,  # Optional field, not provided by the frontend
            tag_number=tag_number,
            notes=notes
        )

        # Add the cow to the database
        session.add(new_cow)
        session.commit()

        return jsonify({"message": "Cow added successfully", "cow_id": new_cow.id}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500

## Purpose :- Get list of Cows Breeds (and the number of cows of that breed) 
# owned by the farmer
@api.route('/get_cow_breeds_owned/<uid>', methods=['GET'])
def get_cow_breeds_ownded(uid):
    # Validate that the uid (oauthID) is provided
    if not uid:
        return jsonify({"error": "Farmer Uid was not provided"}), 400

    # Resolve oauthID to user ID
    user = session.query(User).filter(User.oauthID == uid).first()
    if not user:
        return jsonify({"error": "Farmer not found"}), 404

    try:
        # Query the breeds and count of cows owned by the user
        breeds = (
            session.query(CowBreed.breed, CowBreed.id, func.count(Cow.id).label('count'))
            .join(Cow, Cow.breed_id == CowBreed.id)
            .filter(Cow.owner_id == user.id)  # Use the resolved user ID
            .group_by(CowBreed.id, CowBreed.breed)
            .all()
        )
        # Format the result as a list of dictionaries
        result = [{"breed": breed.breed, "count": breed.count} for breed in breeds]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
## Purpose :- Get list of Cows owned by the farmer in a specific breed
@api.route('/get_cows_by_breed/<uid>/<breed>', methods=['GET'])
def get_cows_by_breed(uid, breed):
    if not uid or not breed:
        return jsonify({"error": "Farmer Uid or Breed name was not provided"}), 400

    # Validate user existence
    user = session.query(User).filter(User.oauthID == uid).first()
    if not user:
        return jsonify({"error": "Farmer not found"}), 404

    # Validate breed existence
    breed_obj = session.query(CowBreed).filter(func.lower(CowBreed.breed) == breed.lower()).first()
    if not breed_obj:
        return jsonify({"error": "Breed not found"}), 404

    try:
        # Query cows owned by the user and of the specified breed
        cows = session.query(Cow).filter(Cow.owner_id == user.id, Cow.breed_id == breed_obj.id).all()

        # Manually construct the response for each cow
        result = []
        for cow in cows:
            result.append({
                "id": cow.id,
                "owner_id": cow.owner_id,
                "name": cow.name,
                "breed_id": cow.breed_id,
                "dob": cow.dob.isoformat() if cow.dob else None,
                "health_status": cow.health_status,
                "milk_production": cow.milk_production,
                "work": cow.work,
                "last_milked": cow.last_milked.isoformat() if cow.last_milked else None,
                "last_fed": cow.last_fed.isoformat() if cow.last_fed else None,
                "height": cow.height,
                "weight": cow.weight,
                "age": cow.age,
                "tag_number": cow.tag_number,
                "notes": cow.notes
            })

        return jsonify(result), 200
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

@api.route('/get_cows/<uid>', methods=['GET'])
def get_cows(uid):
    if not uid:
        return jsonify({"error": "Farmer Uid was not provided"}), 400

    # Validate user existence
    user = session.query(User).filter(User.oauthID == uid).first()
    if not user:
        return jsonify({"error": "Farmer not found"}), 404

    try:
        # Query all cows owned by the user
        cows = session.query(Cow).join(CowBreed, Cow.breed_id == CowBreed.id).filter(Cow.owner_id == user.id).all()

        # Manually construct the response for each cow
        result = []
        for cow in cows:
            result.append({
                "id": cow.id,
                "name": cow.name,
                "breed": cow.breed.breed,  # Fetch breed name from the relationship
                "dob": cow.dob.isoformat() if cow.dob else None,
                "health_status": cow.health_status,
                "milk_production": cow.milk_production,
                "work": cow.work,
                "last_milked": cow.last_milked.isoformat() if cow.last_milked else None,
                "last_fed": cow.last_fed.isoformat() if cow.last_fed else None,
                "height": cow.height,
                "weight": cow.weight,
                "age": cow.age,
                "tag_number": cow.tag_number,
                "notes": cow.notes
            })

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@api.route('/get_cow_by_name/<uid>/<cow_name>', methods=['GET'])
def get_cow_by_name(uid, cow_name):
    """
    Fetch detailed information about a cow by its name for a specific user.
    """
    if not uid or not cow_name:
        return jsonify({"error": "User UID or Cow Name was not provided"}), 400

    try:
        # Validate user existence
        user = session.query(User).filter(User.oauthID == uid).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Fetch cow details by name and owner
        cow = (
            session.query(Cow)
            .options(joinedload(Cow.breed))  # Eager load breed relationship
            .filter(Cow.owner_id == user.id, Cow.name.ilike(cow_name))
            .first()
        )

        if not cow:
            return jsonify({"error": "Cow not found"}), 404

        # Construct response
        cow_data = {
            "id": cow.id,
            "name": cow.name,
            "breed": cow.breed.breed if cow.breed else None,
            "origin": cow.breed.origin if cow.breed else None,
            "age": cow.age,
            "weight": cow.weight,
            "height": cow.height,
            "milkYield": cow.milk_production,
            "lastMilked": cow.last_milked.isoformat() if cow.last_milked else None,
            "lastFed": cow.last_fed.isoformat() if cow.last_fed else None,
            "status": cow.health_status,
            "notes": cow.notes,
        }

        return jsonify(cow_data), 200

    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500
    
@api.route('/get_user/<uid>', methods=['GET'])
def get_user(uid):
    """
    Fetch user information based on the provided uid (OAuth ID).
    """
    if not uid:
        return jsonify({"error": "User UID was not provided"}), 400

    try:
        # Query the user by OAuth ID
        user = session.query(User).filter(User.oauthID == uid).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Construct the response with user details
        user_data = {
            "id": user.id,
            "oauthID": user.oauthID,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "location": user.location,
        }

        return jsonify(user_data), 200

    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500
    
@api.route('/get_locations_with_roles', methods=['GET'])
def get_locations_with_roles():
    """
    Fetch all unique locations stored in the database along with the corresponding roles,
    excluding roles 'Public', 'Normal', NULL roles, and invalid locations.
    """
    try:
        # Query unique locations and roles from the User table, excluding unwanted roles and locations
        locations_with_roles = (
            session.query(User.location, User.role)
            .filter(
                ~User.role.in_(['Public', 'Normal']),  # Exclude 'Public' and 'Normal'
                User.role.isnot(None),                 # Exclude NULL roles
                User.location.isnot(None),             # Exclude NULL locations
                User.location != ''                    # Exclude empty string locations
            )
            .distinct(User.location, User.role)
            .all()
        )

        # Format the response as a list of dictionaries
        result = [
            {"location": location, "role": role}
            for location, role in locations_with_roles
        ]

        return jsonify(result), 200
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500
    
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of Earth in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

@api.route('/notify_nearby_users', methods=['POST'])
def notify_nearby_users():
    data = request.json
    latitude = data['latitude']
    longitude = data['longitude']
    radius_km = data.get('radius_km', 10)  # Default radius is 10 km

    # Query users with specific roles
    users = session.query(User).filter(User.role.in_(['Farmer', 'NGO', 'Gaushala'])).all()

    # Filter users within the radius
    nearby_users = []
    for user in users:
        if user.location:
            try:
                # Extract latitude and longitude from the Google Maps URL
                query_string = user.location.split('q=')[-1]
                user_lat, user_lon = map(float, query_string.split(','))
                distance = haversine(latitude, longitude, user_lat, user_lon)
                if distance <= radius_km:
                    nearby_users.append(user)
            except (ValueError, IndexError):
                # Skip users with invalid location format
                continue

    # Save notifications in the database
    for user in nearby_users:
        notification = Notification(
            user_id=user.id,
            message="A stray cow has been reported near your location.",
            latitude=latitude,
            longitude=longitude
        )
        session.add(notification)

    session.commit()
    return jsonify({'message': 'Notifications sent to nearby users', 'nearby_users': [user.name for user in nearby_users]})

@api.route('/get_notifications/<uid>', methods=['GET'])
def get_notifications(uid):
    notifications = (
        session.query(Notification)
        .join(User, Notification.user_id == User.id)
        .filter(User.oauthID == uid)
        .order_by(Notification.created_at.desc())
        .all()
    )

    return jsonify([
        {
            'message': n.message,
            'latitude': n.latitude,
            'longitude': n.longitude,
            'created_at': n.created_at.isoformat(),
            'image_url': n.image_url,  # Added image_url
            'status': n.status         # Added status
        } for n in notifications
    ])