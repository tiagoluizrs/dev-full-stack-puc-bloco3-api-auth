from models.User import db, User
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

def extract_user_id_from_expired_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'], options={"verify_exp": False})
        return payload.get('user_id')
    except jwt.InvalidTokenError:
        return None

def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(minutes=60)
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
        return {'error': 'Preencha todos os campos'}, 400
    if User.query.filter(User.email == email).first():
        return {'error': 'E-mail já existe'}, 409
    if User.query.filter(User.username == username).first():
        return {'error': 'Username já existe'}, 409
    hashed_pw = hash_password(password)
    user = User(email=email, username=username, password=hashed_pw)
    db.session.add(user)
    db.session.commit()
    return {'message': 'Usuário registrado com sucesso'}, 201

def login_user(data):
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    if not password or (not email and not username):
        return {'error': 'Preencha todos os campos'}, 400
    user = None
    if email:
        user = User.query.filter_by(email=email).first()
    elif username:
        user = User.query.filter_by(username=username).first()

    if not user:
        return {'error': 'Dados inválidos.'}, 401

    if not verify_password(password, user.password):
        return {'error': 'Dados inválidos.'}, 401

    token = generate_token(user.id)
    return {'token': token, 'user': {
        'id': user.id,
        'email': user.email,
        'username': user.username
    }}, 200

def validate_user_token(data):
    token = data.get('token')
    if not token:
        return {'error': 'Token ausente'}, 400
    user_id = extract_user_id_from_expired_token(token)
    is_valid = validate_token(token) is not None
    if not user_id:
        return {'error': 'Token inválido'}, 401
    elif user_id and not is_valid:
        return {'error': 'Token expirado'}, 401
    return {'user_id': user_id}, 200

def reset_user_token(data):
    token = data.get('token')
    if not token:
        return {'error': 'Token ausente.'}, 400
    user_id = extract_user_id_from_expired_token(token)
    if not user_id:
        return {'error': 'Token inválido'}, 401
    new_token = generate_token(user_id)
    return {'token': new_token}, 200