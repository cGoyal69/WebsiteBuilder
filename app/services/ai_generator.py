import openai
import json
from app.config import Config

openai.api_key = Config.OPENAI_API_KEY

class AIGenerator:
    @staticmethod
    def correct_template_type(business_type, original_type):
        type_map = {
    # Bakery & Food Businesses
    "bakery": "bakery",
    "cake": "bakery",
    "pastry": "bakery",
    "cupcake": "bakery",
    "dessert": "bakery",
    "confectionery": "bakery",
    "patisserie": "bakery",
    "cafe": "bakery",
    "bistro": "bakery",
    "coffee": "bakery",
    "sweet": "bakery",
    "chocolate": "bakery",
    "donut": "bakery",
    "bread": "bakery",
    "cookie": "bakery",
    "food truck": "bakery",
    "catering": "bakery",

    # Wedding & Event Businesses
    "wedding": "wedding",
    "event": "wedding",
    "event planner": "wedding",
    "decor": "wedding",
    "florist": "wedding",
    "bridal": "wedding",
    "photography": "wedding",
    "videography": "wedding",
    "dj": "wedding",
    "catering services": "wedding",
    "makeup artist": "wedding",
    "venue": "wedding",
    "banquet": "wedding",
    "invitation": "wedding",
    "marriage": "wedding",
    "ceremony": "wedding",
    "event management": "wedding",

    # Portfolio-based Professionals
    "portfolio": "portfolio",
    "freelancer": "portfolio",
    "developer": "portfolio",
    "designer": "portfolio",
    "graphic designer": "portfolio",
    "photographer": "portfolio",
    "artist": "portfolio",
    "illustrator": "portfolio",
    "videographer": "portfolio",
    "writer": "portfolio",
    "copywriter": "portfolio",
    "editor": "portfolio",
    "musician": "portfolio",
    "tattoo artist": "portfolio",
    "craftsman": "portfolio",
    "architect": "portfolio",
    "interior designer": "portfolio",
    "stylist": "portfolio",

    # Education / Blog
    "education": "blog",
    "school": "blog",
    "college": "blog",
    "university": "blog",
    "teacher": "blog",
    "tutor": "blog",
    "coaching": "blog",
    "learning": "blog",
    "institute": "blog",
    "course": "blog",
    "e-learning": "blog",
    "academy": "blog",
    "training": "blog",
    "educator": "blog",
    "student": "blog",
    "study": "blog",
    "professor": "blog",
    "lecturer": "blog",
    "knowledge": "blog",
    "blog": "blog",
    "newsletter": "blog",
    "publication": "blog",
    "personal blog": "blog",
    "journal": "blog",
    "content creator": "blog",
    "writer blog": "blog",

    # IT / Tech / Corporate
    "it": "it",
    "tech": "it",
    "technology": "it",
    "software": "it",
    "startup": "it",
    "saas": "it",
    "web development": "it",
    "mobile app": "it",
    "cloud": "it",
    "cybersecurity": "it",
    "consulting": "it",
    "blockchain": "it",
    "ai": "it",
    "artificial intelligence": "it",
    "machine learning": "it",
    "data science": "it",
    "big data": "it",
    "api": "it",
    "digital agency": "it",
    "it services": "it",
    "networking": "it",
    "iot": "it",
    "automation": "it",
    "robotics": "it",
    "biotech": "it",
    "fintech": "it",
    "cloud services": "it",
    "hosting": "it",
    "enterprise": "it"
}

        for keyword, mapped_type in type_map.items():
            if keyword in business_type.lower():
                return mapped_type

        return original_type if original_type in ["portfolio", "bakery", "it", "wedding", "blog"] else "it"

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