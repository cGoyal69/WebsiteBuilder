import openai
import json
from app.config import Config

openai.api_key = Config.OPENAI_API_KEY

class AIGenerator:
    @staticmethod
    def generate_website_content(business_type, industry, description, location, logo_tagline):
        # Dummy response for now
        return {
            "hero": {
                "title": f"Welcome to your {business_type}",
                "subtitle": f"{description}",
            },
            "about": {
                "title": f"About Our {industry} Work",
                "content": f"We are located in {location}. Our tagline: {logo_tagline}."
            },
            "services": [
                {"name": "Service 1", "description": "High-quality service 1."},
                {"name": "Service 2", "description": "Reliable service 2."}
            ],
            "contact": {
                "email": "info@example.com",
                "phone": "+91-9876543210"
            }
        }

@staticmethod
def generate_website_content(business_type, industry, description="", location="", logo_tagline=""):
        try:
            prompt = f"""
You are a professional website content generator. Based on the following business details, generate complete JSON content:

Business Type: {business_type}
Industry: {industry}
Location: {location}
Description: {description}
Logo Tagline: {logo_tagline}

Return a JSON object with the following keys:
- heroTitle
- heroSubtitle
- aboutTitle
- aboutContent (2-3 paragraphs)
- services (3-4 services with 'title' and 'description')
- contactText
- companyName
- tagline
- templateType: Choose one from ["portfolio", "bakery", "it", "wedding", "blog"] that fits best.

Respond with **valid JSON only**. Do not add code block markers.
"""

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates structured website content."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )

            content_text = response.choices[0].message.content.strip()
            print("GPT Raw Response:\n", content_text)

            if content_text.startswith("```json"):
                content_text = content_text[7:-3]

            try:
                content = json.loads(content_text)
            except json.JSONDecodeError:
                content = {}

            # Ensure templateType is correct
            content["templateType"] = AIGenerator.correct_template_type(business_type, content.get("templateType", "it"))

            # Fallback defaults if parsing fails
            if not content:
                content = {
                    "heroTitle": f"Premium {business_type.title()} Services",
                    "heroSubtitle": f"Trusted {business_type} solutions for the {industry} industry",
                    "aboutTitle": "About Us",
                    "aboutContent": f"We are a leading {business_type} specializing in the {industry} industry.",
                    "services": [
                        {"title": "Service 1", "description": "Description of service 1"},
                        {"title": "Service 2", "description": "Description of service 2"},
                        {"title": "Service 3", "description": "Description of service 3"}
                    ],
                    "contactText": "Get in touch with us today",
                    "companyName": f"{industry.title()} {business_type.title()}",
                    "tagline": f"Excellence in {industry}",
                    "templateType": AIGenerator.correct_template_type(business_type, "it")
                }

            return content

        except Exception as e:
            print(f"Error generating content: {str(e)}")
            return {
                "heroTitle": f"Welcome to Our {business_type.title()}",
                "heroSubtitle": f"Serving the {industry} industry with excellence",
                "aboutTitle": "About Our Company",
                "aboutContent": f"We are passionate about providing quality {business_type} services to the {industry} industry.",
                "services": [
                    {"title": "Core Service", "description": "Our main service offering"},
                    {"title": "Additional Services", "description": "Supporting services we provide"}
                ],
                "contactText": "Contact us to learn more",
                "companyName": f"{industry.title()} Solutions",
                "tagline": "Your trusted partner",
                "templateType": AIGenerator.correct_template_type(business_type, "it")
            }