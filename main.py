from flask import Flask, request, jsonify
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

def connect_unix_socket() -> sqlalchemy.engine.base.Engine:
    """Initializes a Unix socket connection pool for a Cloud SQL instance of MySQL."""
    db_user = os.environ["DB_USER"] 
    db_pass = os.environ["DB_PASS"] 
    db_name = os.environ["DB_NAME"] 
    unix_socket_path = "/cloudsql/{}".format(os.environ[
        "INSTANCE_CONNECTION_NAME"
    ])

    pool = sqlalchemy.create_engine(
        # Equivalent URL:
        # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=<socket_path>/<cloud_sql_instance_name>
        sqlalchemy.engine.url.URL.create(
            drivername="mysql+pymysql",
            username=db_user,
            password=db_pass,
            database=db_name,
            query={"unix_socket": unix_socket_path},
        ),
    )
    return pool

engine = connect_unix_socket()
Session = sessionmaker(bind=engine)



# Endpoint to handle requests from React Native
@app.route('/data')
def get_data():
    session = Session()
    try:
        results=session.execute(sqlalchemy.text("SELECT * FROM test"))
        data=[dict(row) for row in results]
        session.close()
        return jsonify(data)
    except Exception as e:
        session.close()
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
