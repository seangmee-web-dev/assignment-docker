from flask import Flask,jsonify,request
import os
import mysql.connector

app = Flask(__name__)

FlASK_ENV = os.getenv("FLASK_ENV","dev")

if FlASK_ENV == 'dev':
    MYSQL_HOST = 'db_dev'
    MYSQL_PASSWORD = 'db4dev$'
    MYSQL_DB = 'dev_db'
else:
    MYSQL_HOST = 'db_test'
    MYSQL_PASSWORD = 'db4test$'
    MYSQL_DB = 'test_db'

import time
import mysql.connector
from mysql.connector import Error

def connect_to_database():
    retries = 5
    while retries > 0:
        try:
            connection = mysql.connector.connect(
                host=MYSQL_HOST,
                user='admin',
                password=MYSQL_PASSWORD,
                database=MYSQL_DB
            )
            if connection.is_connected():
                return connection
        except Error as e:
            print(f"Error: {e}")
            time.sleep(5)
            retries -= 1
    raise Exception("Failed to connect to MySQL after multiple attempts")

# Initialize MySQL connection
db = connect_to_database()

@app.route("/")
def index():
    if FlASK_ENV == 'dev':
        return jsonify({"Message":"Welcone to SDPX for dev"})
    else:
        return jsonify({"Message":"Welcone to SDPX for test"})

@app.route("/users",methods=["GET","POST"])
def user():
    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        age = data.get('age')

        cursor = db.cursor()
        cursor.execute("INSERT INTO USERS (name, age) VALUES (%s, %s)", (name, age))
        db.commit()
        
        return jsonify({"message": "User added successfully!"}), 201
    
    elif request.method == 'GET':
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT uid, name, age FROM USERS")
        users_data = cursor.fetchall()
        return jsonify(users_data)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8081)