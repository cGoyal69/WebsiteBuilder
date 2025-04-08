import datetime
from bson import ObjectId
from app.db import db

class Website:
    @staticmethod
    def create_website(user_id, website_data):
        website = {
            "user_id": user_id,
            "name": website_data.get('name', 'My Website'),
            "business_type": website_data.get('business_type', ''),
            "industry": website_data.get('industry', ''),
            "content": website_data.get('content', {}),
            "template": website_data.get('template', 'business'),
            "created_at": datetime.datetime.utcnow(),
            "updated_at": datetime.datetime.utcnow()
        }
        
        result = db.websites.insert_one(website)
        website['_id'] = str(result.inserted_id)
        return website
    
    @staticmethod
    def get_website(website_id):
        website = db.websites.find_one({"_id": ObjectId(website_id)})
        if website:
            website['_id'] = str(website['_id'])
        return website
    
    @staticmethod
    def get_user_websites(user_id):
        websites = list(db.websites.find({"user_id": user_id}))
        for website in websites:
            website['_id'] = str(website['_id'])
        return websites
    
    @staticmethod
    def update_website(website_id, website_data):
        website_data['updated_at'] = datetime.datetime.utcnow()
        
        result = db.websites.update_one(
            {"_id": ObjectId(website_id)},
            {"$set": website_data}
        )
        
        if result.modified_count:
            return Website.get_website(website_id)
        return None
    
    @staticmethod
    def delete_website(website_id):
        result = db.websites.delete_one({"_id": ObjectId(website_id)})
        return result.deleted_count > 0