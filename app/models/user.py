import datetime
import bcrypt
from bson import ObjectId
from app.db import db

class User:
    @staticmethod
    def create_user(email, password):
        if db.users.find_one({"email": email}):
            return None

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = {
            "email": email,
            "password": hashed_password,
            "created_at": datetime.datetime.utcnow(),
            "websites": []
        }

        result = db.users.insert_one(user)
        user['_id'] = str(result.inserted_id)
        return user

    @staticmethod
    def get_user_by_email(email):
        user = db.users.find_one({"email": email})
        if user:
            user['_id'] = str(user['_id'])
        return user

    @staticmethod
    def validate_login(email, password):
        user = db.users.find_one({"email": email})
        if not user:
            return None
        if bcrypt.checkpw(password.encode('utf-8'), user['password']):
            user['_id'] = str(user['_id'])
            return user
        return None

    @staticmethod
    def add_website_to_user(user_id, website_id):
        db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$push": {"websites": str(website_id)}}
        )