import openai
import json
from app.config import Config

openai.api_key = Config.OPENAI_API_KEY

class AIGenerator:
    @staticmethod
    def generate_website_content(business_type, industry):
        """Generate website content based on business type and industry."""
        try:
            # Create a prompt for OpenAI
            prompt = f"""
            Generate website content for a {business_type} in the {industry} industry.
            Format the response as JSON with the following fields:
            - heroTitle (catchy headline)
            - heroSubtitle (brief description)
            - aboutTitle 
            - aboutContent (2-3 paragraphs about the business)
            - services (list of 3-4 services with title and description for each)
            - contactText (brief invitation to contact)
            - companyName (a creative business name)
            - tagline (a short slogan)
            - templateType (choose from: portfolio, bakery, it, wedding, blog)
            """

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates website content in JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )

            content_text = response.choices[0].message.content.strip()

            if content_text.startswith("```json"):
                content_text = content_text[7:-3]  # Remove markdown markers

            try:
                content = json.loads(content_text)
            except json.JSONDecodeError:
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
                    "templateType": "it"
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
                "templateType": "it"
            }
