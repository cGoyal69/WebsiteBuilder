
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"message": "Email and password are required"}), 400
    
    user = User.create_user(data['email'], data['password'])
    if not user:
        return jsonify({"message": "User already exists"}), 400
    
    # Remove password from response
    user.pop('password', None)
    
    return jsonify({
        "message": "User registered successfully",
        "user": user
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"message": "Email and password are required"}), 400
    
    user = User.validate_login(data['email'], data['password'])
    if not user:
        return jsonify({"message": "Invalid credentials"}), 401
    
    # Create JWT token
    access_token = create_access_token(identity=str(user['_id']))
    
    return jsonify({
        "message": "Login successful",
        "token": access_token,
        "user_id": str(user['_id']),
        "email": user['email']
    }), 200

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    user = User.get_user_by_email(current_user_id)
    
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    # Remove password from response
    user.pop('password', None)
    
    return jsonify({
        "user": user
    }), 200