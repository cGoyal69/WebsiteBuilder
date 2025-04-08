from app import create_app
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Create Flask app using factory pattern
app = create_app()

# Optional: Push context (if doing stuff outside request, like CLI/db scripts)
app.app_context().push()

# Optional: Print Mongo URI to verify
print("MongoDB URI in use:", app.config.get("MONGO_URI"))

# Entry point
if __name__ == '__main__':
    app.run(debug=True)