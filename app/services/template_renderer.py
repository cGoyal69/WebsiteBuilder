
from flask import render_template
import os
import json

class TemplateRenderer:
    @staticmethod
    def get_available_templates():
        """Return list of available templates."""
        template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'templates')
        return [name for name in os.listdir(template_dir) if os.path.isdir(os.path.join(template_dir, name))]
    
    @staticmethod
    def render_website_preview(website_data):
        """Render website preview based on template and content."""
        template_name = website_data.get('template', 'business')
        content = website_data.get('content', {})
        
        # Render the template with the content
        return render_template(
            'preview_template.html',
            template=template_name,
            content=content,
            website=website_data
        )