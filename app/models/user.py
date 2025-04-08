import datetime
import bcrypt
from bson import ObjectId
from app import mongo

class User:
    @staticmethod
    def create_user(email, password):
        # Check if user exists
        if mongo.db.users.find_one({"email": email}):
            return None
        
        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        user = {
            "email": email,
            "password": hashed_password,
            "created_at": datetime.datetime.utcnow(),
            "websites": []
        }
        
        result = mongo.db.users.insert_one(user)
        user['_id'] = str(result.inserted_id)
        return user
    
    @staticmethod
    def get_user_by_email(email):
        user = mongo.db.users.find_one({"email": email})
        if user:
            user['_id'] = str(user['_id'])
        return user
    
    @staticmethod
    def validate_login(email, password):
        user = mongo.db.users.find_one({"email": email})
        if not user:
            return None
        
        if bcrypt.checkpw(password.encode('utf-8'), user['password']):
            user['_id'] = str(user['_id'])
            return user
        return None
    
    @staticmethod
    def add_website_to_user(user_id, website_id):
        mongo.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$push": {"websites": str(website_id)}}
        )