from models.teste import db, User
from passlib.hash import pbkdf2_sha256
import jwt
import os
from datetime import datetime, timedelta

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

def hash_password(password):
    return pbkdf2_sha256.hash(password)

def verify_password(password_no_hash, password_database):
    try:
        return pbkdf2_sha256.verify(password_no_hash, password_database)
    except ValueError:
        return False

def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=2)
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')

def validate_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def register_user(data):
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    if not email or not username or not password:
        return {'error': 'Missing fields'}, 400
    if User.query.filter((User.email == email) | (User.username == username)).first():
        return {'error': 'User already exists'}, 409
    hashed_pw = hash_password(password)
    user = User(email=email, username=username, password=hashed_pw)
    db.session.add(user)
    db.session.commit()
    return {'message': 'User registered successfully'}, 201

def login_user(data):
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    if not password or (not email and not username):
        return {'error': 'Missing fields'}, 400
    user = None
    if email:
        user = User.query.filter_by(email=email).first()
    elif username:
        user = User.query.filter_by(username=username).first()

    if not user:
        return {'error': 'Invalid credentials'}, 401

    if not verify_password(password, user.password):
        return {'error': 'Invalid credentials'}, 401

    token = generate_token(user.id)
    return {'token': token}, 200

def validate_user_token(data):
    token = data.get('token')
    if not token:
        return {'error': 'Missing token'}, 400
    user_id = validate_token(token)
    if not user_id:
        return {'error': 'Invalid or expired token'}, 401
    return {'user_id': user_id}, 200

