from flask import Flask, request, jsonify
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from db_connect import session,Session
from views import api
from chatbot import chat_api
from breedingRecBot import breeding_rec_api
import os

app = Flask(__name__)

app.register_blueprint(api) # from views.py
app.register_blueprint(chat_api)
app.register_blueprint(breeding_rec_api)

# Endpoint to handle requests from React Native
@app.route('/data')
def get_data():
    try:
        results=session.execute(sqlalchemy.text("SELECT * FROM test"))
        data = []
        for row in results:
            row_dict = dict(row._mapping)
            data.append(row_dict)
        print(data)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.teardown_appcontext
def shutdown_session(exception=None):
    if exception:
        session.rollback()
    Session.remove()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
