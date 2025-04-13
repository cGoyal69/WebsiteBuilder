# AI-Driven Website Builder

An intelligent application that uses AI to generate and customize websites based on business requirements.

## Overview

This AI-Driven Website Builder leverages artificial intelligence to create professional websites tailored to your business needs. Simply provide details about your business, and the application will generate a complete website with appropriate content, design, and structure.

## Features

- **AI-Generated Content**: Automatically create website content based on your business type and industry
- **Template Selection**: Choose from various professional templates
- **Easy Customization**: Modify AI-generated content to fit your specific needs
- **Responsive Design**: All websites are mobile-friendly and work across devices
- **User Management**: Create an account to save and manage multiple websites
- **Live Preview**: See changes in real-time as you edit your website

## Getting Started

### Prerequisites

- Python 3.8+
- MongoDB (local instance or MongoDB Atlas)
- OpenAI API key

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-website-builder.git
   cd ai-website-builder
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   
   Create a `.env` file in the project root with:
   ```
   SECRET_KEY=your_secret_key
   JWT_SECRET_KEY=your_jwt_secret
   MONGO_URI=mongodb://localhost:27017/website_builder
   OPENAI_API_KEY=your_openai_api_key
   ```

5. Start MongoDB (if using locally):
   ```bash
   mongod --dbpath /path/to/data/directory
   ```

6. Run the application:
   ```bash
   python run.py
   ```

7. Access the application at `http://localhost:5000`

## Usage

1. Register for an account through the `register.html` page
2. Log in through the `login.html` page
3. After login, you'll be directed to `builder.html` where you can:
   - Create a new website
   - Choose industry and business type
   - Customize content
   - Preview your website
   - Save your work

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

## Development

### Project Structure
```
ai-website-builder/
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── static/
│   └── templates/
├── config.py
├── requirements.txt
└── run.py
```

### Testing

Run tests using pytest:
```bash
pytest
```

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature/my-new-feature`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for providing the AI models
- Contributors and open-source projects that made this possible