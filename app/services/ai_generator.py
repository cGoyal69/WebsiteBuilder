import openai
import json
from app.config import Config

openai.api_key = Config.OPENAI_API_KEY

class AIGenerator:
    @staticmethod
    def correct_template_type(business_type, fallback="it"):
        mapping = {
            "portfolio": ["portfolio", "freelancer", "photography", "resume"],
            "bakery": ["bakery", "cake", "baking", "food"],
            "it": ["software", "it", "tech", "saas", "web", "development"],
            "wedding": ["wedding", "event", "planner", "ceremony"],
            "blog": ["blog", "news", "magazine", "article"]
        }

        for key, keywords in mapping.items():
            if any(k in business_type.lower() for k in keywords):
                return key
        return fallback

    @staticmethod
    def generate_website_content(business_type, industry, description="", location="", logo_tagline=""):
        try:
            prompt = f"""
You are a professional website content generator. Based on the following business details, generate complete JSON content give 2-3 paras where required and dont change name of company, it is decided by user:

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
- templateType (one of: portfolio, bakery, it, wedding, blog)

Respond with valid JSON only. No markdown, no explanation, no extra text.
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

            # Parse and clean
            if content_text.startswith("```json"):
                content_text = content_text[7:-3].strip()

            content = json.loads(content_text)
            content["templateType"] = AIGenerator.correct_template_type(business_type, content.get("templateType", "it"))

            return content

        except Exception as e:
            print(f"❌ Error generating content: {str(e)}")
            return {
                "heroTitle": f"Welcome to Our {business_type.title()}",
                "heroSubtitle": f"Serving the {industry} industry with excellence",
                "aboutTitle": "About Our Company",
                "aboutContent": f"We provide top-notch {business_type} services in the {industry} space.",
                "services": [
                    {"title": "Consulting", "description": "Expert guidance tailored to your needs"},
                    {"title": "Implementation", "description": "Full-scale solution deployment"},
                    {"title": "Support", "description": "Ongoing maintenance and support"}
                ],
                "contactText": "Reach out to us for more information.",
                "companyName": f"{industry.title()} Experts",
                "tagline": logo_tagline or "Committed to Quality",
                "templateType": AIGenerator.correct_template_type(business_type, "it")
            }