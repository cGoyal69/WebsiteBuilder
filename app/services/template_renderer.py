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
        """Render website preview based on template type and content."""
        content = website_data.get('content', {})
        template_type = content.get('templateType', 'default')  # e.g., 'portfolio', 'bakery', 'it'
        
        # Fallback to default template if specific one not found
        preview_template = f'preview_{template_type}.html'
        template_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            'templates', 
            preview_template
        )
        
        # Check if template file exists
        if not os.path.exists(template_path):
            preview_template = 'preview_default.html'  # fallback template
        
        return render_template(
            preview_template,
            template=template_type,
            content=content,
            website=website_data
        )