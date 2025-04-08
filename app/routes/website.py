
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.website import Website
from app.models.user import User
from app.services.ai_generator import AIGenerator
from app.security import rate_limit, validate_website_data
from app.caching import cache, invalidate_cache_for_website, invalidate_cache_for_user

website_bp = Blueprint('website', __name__, url_prefix='/api/websites')

@website_bp.route('/', methods=['POST'])
@jwt_required()
@rate_limit(requests_per_minute=10)
def create_website():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data:
        return jsonify({"message": "No data provided"}), 400
    
    # Validate input data
    errors = validate_website_data(data)
    if errors:
        return jsonify({"message": "Validation errors", "errors": errors}), 400
        
    # Generate AI content if business_type and industry are provided
    if 'business_type' in data and 'industry' in data:
        content = AIGenerator.generate_website_content(
            data['business_type'], 
            data['industry']
        )
        data['content'] = content
    
    # Create website in database
    website = Website.create_website(current_user_id, data)
    
    # Associate website with user
    User.add_website_to_user(current_user_id, website['_id'])
    
    # Invalidate any cached website lists for this user
    invalidate_cache_for_user(current_user_id)
    
    return jsonify({
        "message": "Website created successfully",
        "website": website
    }), 201

@website_bp.route('/', methods=['GET'])
@jwt_required()
@rate_limit(requests_per_minute=30)
@cache(timeout=60)  # Cache for 1 minute
def get_user_websites():
    current_user_id = get_jwt_identity()
    websites = Website.get_user_websites(current_user_id)
    
    return jsonify({
        "websites": websites
    }), 200

@website_bp.route('/<website_id>', methods=['GET'])
@jwt_required()
@rate_limit(requests_per_minute=30)
@cache(timeout=300)  # Cache for 5 minutes
def get_website(website_id):
    website = Website.get_website(website_id)
    
    if not website:
        return jsonify({"message": "Website not found"}), 404
        
    return jsonify({
        "website": website
    }), 200

@website_bp.route('/<website_id>', methods=['PUT'])
@jwt_required()
@rate_limit(requests_per_minute=20)
def update_website(website_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data:
        return jsonify({"message": "No data provided"}), 400
    
    # Validate input data
    errors = validate_website_data(data)
    if errors:
        return jsonify({"message": "Validation errors", "errors": errors}), 400
        
    # Verify ownership
    website = Website.get_website(website_id)
    if not website or website['user_id'] != current_user_id:
        return jsonify({"message": "Website not found or access denied"}), 404
    
    # Update website
    updated_website = Website.update_website(website_id, data)
    
    # Invalidate cache for this website
    invalidate_cache_for_website(website_id)
    
    return jsonify({
        "message": "Website updated successfully",
        "website": updated_website
    }), 200

@website_bp.route('/<website_id>', methods=['DELETE'])
@jwt_required()
@rate_limit(requests_per_minute=10)
def delete_website(website_id):
    current_user_id = get_jwt_identity()
    
    # Verify ownership
    website = Website.get_website(website_id)
    if not website or website['user_id'] != current_user_id:
        return jsonify({"message": "Website not found or access denied"}), 404
    
    # Delete website
    success = Website.delete_website(website_id)
    
    if success:
        # Invalidate caches
        invalidate_cache_for_website(website_id)
        invalidate_cache_for_user(current_user_id)
        
        return jsonify({
            "message": "Website deleted successfully"
        }), 200
    else:
        return jsonify({
            "message": "Failed to delete website"
        }), 500

@website_bp.route('/<website_id>/regenerate', methods=['POST'])
@jwt_required()
@rate_limit(requests_per_minute=5)
def regenerate_content(website_id):
    current_user_id = get_jwt_identity()
    
    # Verify ownership
    website = Website.get_website(website_id)
    if not website or website['user_id'] != current_user_id:
        return jsonify({"message": "Website not found or access denied"}), 404
    
    # Regenerate content with AI
    content = AIGenerator.generate_website_content(
        website.get('business_type', ''), 
        website.get('industry', '')
    )
    
    # Update website with new content
    website['content'] = content
    updated_website = Website.update_website(website_id, website)
    
    # Invalidate cache for this website
    invalidate_cache_for_website(website_id)
    
    return jsonify({
        "message": "Website content regenerated successfully",
        "website": updated_website
    }), 200