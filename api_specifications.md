# API Specifications

## 1. Add User
**Endpoint:** `/add_user`  
**Method:** `POST`  
**Description:** Adds a new user to the database after signup.  
**Request Body:**  
```json
{
  "oauthID": "string",
  "name": "string",
  "role": "string",
  "email": "string",
  "location": "string"
}
```  
**Responses:**
- `200 OK`: User added successfully.
- `400 Bad Request`: Missing required fields or user already exists.
- `500 Internal Server Error`: Error occurred during database operation.

---

## 2. Get All Breeds
**Endpoint:** `/get_breeds`  
**Method:** `GET`  
**Description:** Retrieves a list of all cow breeds.  
**Responses:**
- `200 OK`: List of breed names.
- `500 Internal Server Error`: Error occurred during database operation.

---

## 3. Add Cow
**Endpoint:** `/add_cow`  
**Method:** `POST`  
**Description:** Adds a cow owned by a farmer.  
**Request Body:**  
```json
{
  "name": "string",
  "breed": "string",
  "birthDate": "YYYY-MM-DD",
  "owner_id": "string",
  "milk_production": "float",
  "tagNumber": "string",
  "notes": "string"
}
```  
**Responses:**
- `201 Created`: Cow added successfully.
- `400 Bad Request`: Missing required fields.
- `404 Not Found`: User or breed not found.
- `500 Internal Server Error`: Error occurred during database operation.

---

## 4. Get Cow Breeds Owned
**Endpoint:** `/get_cow_breeds_owned/<uid>`  
**Method:** `GET`  
**Description:** Retrieves a list of cow breeds and their counts owned by a specific user.  
**Path Parameters:**
- `uid`: User's OAuth ID.  
**Responses:**
- `200 OK`: List of breeds and their counts.
- `400 Bad Request`: Missing UID.
- `404 Not Found`: User not found.
- `500 Internal Server Error`: Error occurred during database operation.

---

## 5. Get Cows by Breed
**Endpoint:** `/get_cows_by_breed/<uid>/<breed>`  
**Method:** `GET`  
**Description:** Retrieves a list of cows owned by a user for a specific breed.  
**Path Parameters:**
- `uid`: User's OAuth ID.
- `breed`: Breed name.  
**Responses:**
- `200 OK`: List of cows.
- `400 Bad Request`: Missing UID or breed.
- `404 Not Found`: User or breed not found.
- `500 Internal Server Error`: Error occurred during database operation.

---

## 6. Get Cow Details
**Endpoint:** `/get_cow/<int:cow_id>`  
**Method:** `GET`  
**Description:** Retrieves details of a specific cow by its ID.  
**Path Parameters:**
- `cow_id`: Cow ID.  
**Responses:**
- `200 OK`: Cow details.
- `400 Bad Request`: Missing cow ID.
- `404 Not Found`: Cow not found.

---

## 7. Get Breed Details
**Endpoint:** `/get_breed/<int:breed_id>`  
**Method:** `GET`  
**Description:** Retrieves details of a specific breed by its ID.  
**Path Parameters:**
- `breed_id`: Breed ID.  
**Responses:**
- `200 OK`: Breed details.
- `400 Bad Request`: Missing breed ID.
- `404 Not Found`: Breed not found.

---

## 8. Set User Role
**Endpoint:** `/set_role`  
**Method:** `POST`  
**Description:** Updates the role of a specific user.  
**Request Body:**  
```json
{
  "uid": "string",
  "role": "string"
}
```  
**Responses:**
- `200 OK`: Role updated successfully.
- `400 Bad Request`: Missing UID or role.
- `404 Not Found`: User not found.
- `500 Internal Server Error`: Error occurred during database operation.

---

## 9. Get User Role
**Endpoint:** `/get_role/<uid>`  
**Method:** `GET`  
**Description:** Retrieves the role of a specific user.  
**Path Parameters:**
- `uid`: User's OAuth ID.  
**Responses:**
- `200 OK`: User role.
- `400 Bad Request`: Missing UID.
- `404 Not Found`: User not found.
- `500 Internal Server Error`: Error occurred during database operation.

---

## 10. Get All Cows
**Endpoint:** `/get_cows/<uid>`  
**Method:** `GET`  
**Description:** Retrieves all cows owned by a specific user.  
**Path Parameters:**
- `uid`: User's OAuth ID.  
**Responses:**
- `200 OK`: List of cows.
- `400 Bad Request`: Missing UID.
- `404 Not Found`: User not found.
- `500 Internal Server Error`: Error occurred during database operation.

---

## 11. Get Cow by Name
**Endpoint:** `/get_cow_by_name/<uid>/<cow_name>`  
**Method:** `GET`  
**Description:** Retrieves details of a cow by its name for a specific user.  
**Path Parameters:**
- `uid`: User's OAuth ID.
- `cow_name`: Cow name.  
**Responses:**
- `200 OK`: Cow details.
- `400 Bad Request`: Missing UID or cow name.
- `404 Not Found`: User or cow not found.
- `500 Internal Server Error`: Error occurred during database operation.

---

## 12. Get User Details
**Endpoint:** `/get_user/<uid>`  
**Method:** `GET`  
**Description:** Retrieves details of a specific user.  
**Path Parameters:**
- `uid`: User's OAuth ID.  
**Responses:**
- `200 OK`: User details.
- `400 Bad Request`: Missing UID.
- `404 Not Found`: User not found.
- `500 Internal Server Error`: Error occurred during database operation.

---

## 13. Get Locations with Roles
**Endpoint:** `/get_locations_with_roles`  
**Method:** `GET`  
**Description:** Retrieves unique locations and roles, excluding invalid roles and locations.  
**Responses:**
- `200 OK`: List of locations and roles.
- `500 Internal Server Error`: Error occurred during database operation.

---

## 14. Notify Nearby Users
**Endpoint:** `/notify_nearby_users`  
**Method:** `POST`  
**Description:** Sends notifications to users within a specified radius.  
**Request Body:**  
```json
{
  "latitude": "float",
  "longitude": "float",
  "radius_km": "float",
  "image_url": "string",
  "status": "string"
}
```  
**Responses:**
- `200 OK`: Notifications sent successfully.
- `500 Internal Server Error`: Error occurred during database operation.

---

## 15. Get Notifications
**Endpoint:** `/get_notifications/<uid>`  
**Method:** `GET`  
**Description:** Retrieves notifications for a specific user.  
**Path Parameters:**
- `uid`: User's OAuth ID.  
**Responses:**
- `200 OK`: List of notifications.
- `500 Internal Server Error`: Error occurred during database operation.

---

## 16. Get Cow Count by Breed
**Endpoint:** `/get_cow_count_by_breed/<uid>/<breed>`  
**Method:** `GET`  
**Description:** Retrieves the count of cows under a specific breed for a user.  
**Path Parameters:**
- `uid`: User's OAuth ID.
- `breed`: Breed name.  
**Responses:**
- `200 OK`: Cow count.
- `400 Bad Request`: Missing UID or breed.
- `404 Not Found`: User or breed not found.
- `500 Internal Server Error`: Error occurred during database operation.

---

## 17. Update Cow
**Endpoint:** `/update_cow/<uid>/<cow_name>`  
**Method:** `PUT`  
**Description:** Updates specific fields of a cow by its name for a user.  
**Path Parameters:**
- `uid`: User's OAuth ID.
- `cow_name`: Cow name.  
**Request Body:**  
```json
{
  "last_milked": "string",
  "last_fed": "string",
  "notes": "string",
  "milk_production": "float",
  "health_status": "string"
}
```  
**Responses:**
- `200 OK`: Cow updated successfully.
- `400 Bad Request`: Missing UID or cow name.
- `404 Not Found`: User or cow not found.
- `500 Internal Server Error`: Error occurred during database operation.

---

## 18. Delete Cow
**Endpoint:** `/delete_cow/<uid>/<cow_name>`  
**Method:** `DELETE`  
**Description:** Deletes a cow by its name for a specific user.  
**Path Parameters:**
- `uid`: User's OAuth ID.
- `cow_name`: Cow name.  
**Responses:**
- `200 OK`: Cow deleted successfully.
- `400 Bad Request`: Missing UID or cow name.
- `404 Not Found`: User or cow not found.
- `500 Internal Server Error`: Error occurred during database operation.