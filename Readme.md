# AI-Driven Website Builder - Deployment Guide

This guide explains how to set up and run the AI-Driven Website Builder application.

## Prerequisites

- Python 3.8+
- MongoDB (local instance or MongoDB Atlas)
- OpenAI API key

## Setup Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ai-website-builder.git
cd ai-website-builder
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root with the following variables:

```
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret
MONGO_URI=mongodb://localhost:27017/website_builder
OPENAI_API_KEY=your_openai_api_key
```

Replace the placeholder values with your actual configuration.

### 5. Start MongoDB

If using a local MongoDB instance:

```bash
# Start MongoDB service
mongod --dbpath /path/to/data/directory
```

### 6. Run the Application

```bash
python run.py
```

The server will start on `http://localhost:5000`.

##Fronten

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get JWT token

### Website Management
- `POST /api/websites/` - Create a new website
- `GET /api/websites/` - Get all websites for current user
- `GET /api/websites/<website_id>` - Get specific website
- `PUT /api/websites/<website_id>` - Update website
- `DELETE /api/websites/<website_id>` - Delete website
- `POST /api/websites/<website_id>/regenerate` - Regenerate AI content

### Preview
- `GET /preview/templates` - Get available templates
- `GET /preview/<website_id>` - Preview a website

## Testing the Application

1. Register a new user:
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

2. Login to get a token:
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

3. Create a website (using the token):
```bash
curl -X POST http://localhost:5000/api/websites/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"name": "My First Website", "business_type": "bakery", "industry": "food"}'
```

4. Preview your website by opening in a browser:
```
http://localhost:5000/preview/YOUR_WEBSITE_ID
```

