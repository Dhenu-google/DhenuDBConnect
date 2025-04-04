# DhenuDBConnect

DhenuDBConnect is a backend application designed to manage and operate a database for [Project Dhenu](https://github.com/Dhenu-google/dhenu-app). It provides APIs for managing users, cows, breeds, diseases, notifications, and more. It also Provides endpoints for two AI features. The application is containerized using Docker and is designed to run on **Google Cloud Run.**

## Features

- **User Management**: Add, update, and retrieve user information, including roles and locations.
- **Cow Management**: Add, update, delete, and retrieve cows owned by users, including details like breed, health status, and milk production.
- **Breed Management**: Retrieve information about cow breeds and their characteristics.
- **Disease Management**: Track diseases affecting cows and their outcomes.
- **Notifications**: Notify nearby users about events like stray cows or emergencies.
- **Chatbot Integration**: A chatbot API to answer questions related to cow care and breeds.
- **Breeding Recommendations**: Generate breeding recommendations for Indian cow breeds using AI.
- **Database Migrations**: Manage database schema using Alembic.

## Project Structure

```plaintext
main.py - The main Flask application file. It initializes the Flask app, sets up routes, and manages the SQLAlchemy session handler for database interactions.
models.py - Contains SQLAlchemy ORM models that define the database schema (tables and relationships).
views.py - Implements the Flask API endpoints for handling requests and responses.
db_connect.py - Manages database connections, including configuration and initialization of the SQLAlchemy engine.
chatbot.py - Provides the API for the MooAI feature, which integrates a chatbot to answer questions related to cow care and breeds.
breedingRecBot.py - Implements the API for the Breeding Recommendation Bot, which uses AI to suggest breeding strategies for Indian cow breeds.
alembic.ini - Configuration file for Alembic, used for managing database migrations.
Dockerfile - Defines the Docker image for containerizing the application.
entrypoint.sh - A shell script used as the entry point for the Docker container, ensuring proper initialization of the application.
```

## Prerequisites

- Python 3.10 or higher
- Docker
- Google Cloud SDK (for deployment)
- A Google Cloud SQL Instance.
- cloud-sql-proxy to connect to Cloud SQL instance. (for local development)
- `.env` file with the following variables:
```plaintext
DB_USER=<your-database-username>
DB_PASS=<your-database-password>
DB_NAME=<your-database-name>
INSTANCE_CONNECTION_NAME=<your-cloud-sql-instance-connection-name>
GOOGLE_APPLICATION_CREDENTIALS=
```


## Installation
1. **Set Up `cloud-sql-proxy`:**
   - Download the `cloud-sql-proxy` binary from the [official documentation](https://cloud.google.com/sql/docs/mysql/sql-proxy).
   - Run the proxy to connect to your Google Cloud SQL instance:
     ```bash
     ./cloud-sql-proxy --credentials-file <credentials-file-path> --port <port-number> <INSTANCE_CONNECTION_NAME>
     ```
     Replace `<INSTANCE_CONNECTION_NAME>` with the value from your `.env` file.

2. Clone the repository:
 ```bash
 git clone <repository-url>
 cd DhenuDBConnect
 ```
3. Install dependencies:
```bash
(activate venv, then)
pip install -r requirements.txt
```

4. Run database migrations:
Make migrations if needed.
```bash
alembic revision --autogenerate -m "message" 
```
Run Migrations
```bash
alembic upgrade head
```
5. Start the Development Server:
```bash
python main.py
```

## Deployment
Continuous deployment using GitHub and Google Cloud Build.
[Instructions can be found here](https://cloud.google.com/run/docs/continuous-deployment-with-cloud-build)

## API Specifications
[Find it here](/api_specifications.md)

License
This project is licensed under the MIT License. See the [LICENSE](/LICENSE) file for details.
