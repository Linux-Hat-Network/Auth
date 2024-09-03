from flask import Flask, request, jsonify, make_response, render_template, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import date, datetime, timedelta
import math
import string
import random
import subprocess
from requests import get
import os
import bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

CORS(app)

class Keys(db.Model):
    __tablename__ = 'Keys'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    create_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer)

class Users(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    password = db.Column(db.String)
    password_salt = db.Column(db.String)
    is_admin = db.Column(db.Integer)

with app.app_context():
    db.create_all()

# DB
@app.route("/api/key/getinfo", methods=['POST'])
def get_key():
    data = request.get_json()
    key = db.session.query(Keys).filter_by(name=data.get("key")).first()
    if key and key.create_date + timedelta(days=365) > datetime.now():
        key.create_date = datetime.now()
        db.session.commit()
        id = key.user_id
        user = db.session.query(Users).filter_by(id=id).first()
        return jsonify({"key_id":key.id, "key" : key.name, "create_date":key.create_date, "user_id":user.id})
    else :
        return jsonify({"status":"INVALID"})

@app.route("/api/user/<id>")
def get_user(id):
    user = db.session.query(Users).filter_by(id=id).first()
    if user:
        return jsonify({"id":user.id, "name" : user.name, "is_admin":user.is_admin})
    else :
        return jsonify({"status":"FAIL"})

@app.route("/api/new/key", methods=['POST'])
def new_key():
    data = request.get_json()
    user = db.session.query(Users).filter_by(name=data.get("name")).first()
    if user:
        print("test1")
        password = data.get("password")
        salt = user.password_salt
        hach = bcrypt.hashpw(password.encode('utf-8'), salt)
        if hach == user.password:
            print("test2")
            code = ""
            for i in range(32):
                code += random.choice(string.ascii_lowercase+string.digits+string.digits)
            key = Keys(name=code, create_date=datetime.now(), user_id=user.id)
            db.session.add(key)
            db.session.commit()
            return jsonify({"key":code, "user_name":user.name, "user_id":user.id})
    return jsonify({"status":"FAIL"})

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def icon():
    return send_file('../static/favicon.ico')

app.run(host="127.0.0.1",port=8081,debug=True)
