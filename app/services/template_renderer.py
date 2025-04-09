from flask import render_template
import os

class TemplateRenderer:
    @staticmethod
    def get_available_templates():
        template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
        return [
            file for file in os.listdir(template_dir)
            if file.startswith('preview_') and file.endswith('.html')
        ]
    
    @staticmethod
    def render_website_preview(website_data):
        content = website_data.get('content', {})
        template_type = content.get('templateType', 'default')

        preview_template = f'preview_{template_type}.html'

        try:
            return render_template(
                preview_template,
                content=content,
                website=website_data
            )
        except Exception as e:
            print(f"⚠️ Failed to render {preview_template}. Falling back to default. Error: {e}")
            return render_template(
                'preview_default.html',
                content=content,
                website=website_data
            )