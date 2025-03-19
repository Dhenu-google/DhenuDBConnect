from flask import Flask, request, jsonify
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from db_connect import session
from views import api
import os
app = Flask(__name__)

app.register_blueprint(api) # from views.py

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
        session.close()
        return jsonify(data)
    except Exception as e:
        session.close()
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
