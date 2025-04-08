
from flask import Blueprint, jsonify, render_template
from app.models.website import Website
from app.services.template_renderer import TemplateRenderer
from app.caching import cache

preview_bp = Blueprint('preview', __name__, url_prefix='/preview')

@preview_bp.route('/templates', methods=['GET'])
@cache(timeout=3600)  # Cache for an hour since templates rarely change
def get_templates():
    templates = TemplateRenderer.get_available_templates()
    return jsonify({
        "templates": templates
    }), 200

@preview_bp.route('/<website_id>', methods=['GET'])
@cache(timeout=60)  # Cache for a minute
def preview_website(website_id):
    website = Website.get_website(website_id)
    
    if not website:
        return jsonify({"message": "Website not found"}), 404
    
    # Render website preview
    return TemplateRenderer.render_website_preview(website)