"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/token', methods=['POST'])
def create_token():
    email = request.json.get('email', None)
    access_token = create_access_token(identity=email)
    
    return jsonify(access_token=access_token)

@api.route('/user', methods=['GET'])
def get_all_users():
    users = User.query.all()
    all_users = list(map(lambda x:x.serialize(), users))

    return jsonify(all_users), 200

@api.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if user is None:
        raise APIException('User not found', status_code=404)
    return jsonify(user.serialize()), 200

@api.route('/signup', methods=['POST'])
def create_user():
    body = request.get_json()
    user = User()
    if 'email' not in body:
        raise APIException('Please provide an email', status_code=400)
    if 'password' not in body:
        raise APIException('Please provide a password', status_code=400)
    user.email=body['email']
    user.password=body['password']
    user.is_active=True
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize()), 200

@api.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    body = request.get_json()
    user = User.query.get(id)
    if user is None:
        raise APIException('User not found', status_code=404)
    if 'email' in body:
        user.email = body['email']
    if 'password' in body:
        user.password = body['password']
    if 'is_active' in body:
        user.is_active = body['is_active']
    db.session.commit()
    return jsonify(user.serialize()), 200

@api.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if user is None:
        raise APIException('User not found', status_code=404)
    db.session.delete(user)
    db.session.commit()
    return jsonify(user.serialize()), 200

@api.route('/private', methods=['GET'])
@jwt_required()
def get_private():
    return jsonify({'msg':'This endpoint is private. You must be logged in to see it.'}), 200
