import os
from datetime import timedelta
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_secret_key')
    MONGO_URI = os.environ.get('MONGODB_URI')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt_secret_key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', 'your-openai-api-key')

# Debug output for testing
if __name__ == '__main__':
    print("Loaded MONGO_URI:", os.environ.get("MONGODB_URI"))