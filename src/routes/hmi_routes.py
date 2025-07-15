from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from src.models.user import db
from src.models.hmi_models import ProfessionalApplication, ClientRequest, ContactInfo, Review
import os
from werkzeug.utils import secure_filename

hmi_bp = Blueprint('hmi', __name__)

# Configure upload folder for profile pictures
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Professional Applications Routes
@hmi_bp.route('/professional-applications', methods=['POST'])
@cross_origin()
def submit_professional_application():
    try:
        data = request.get_json()
        
        # Create new professional application
        application = ProfessionalApplication(
            full_name=data.get('fullName'),
            email=data.get('email'),
            phone=data.get('phone'),
            location=data.get('location'),
            specialty=data.get('specialty'),
            gender=data.get('gender'),
            cv_details=data.get('cvDetails')
        )
        
        db.session.add(application)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Application submitted successfully!',
            'application': application.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error submitting application: {str(e)}'
        }), 500

@hmi_bp.route('/professional-applications', methods=['GET'])
@cross_origin()
def get_professional_applications():
    try:
        applications = ProfessionalApplication.query.order_by(ProfessionalApplication.submitted_at.desc()).all()
        return jsonify({
            'success': True,
            'applications': [app.to_dict() for app in applications]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching applications: {str(e)}'
        }), 500

@hmi_bp.route('/professional-applications/<int:app_id>', methods=['DELETE'])
@cross_origin()
def delete_professional_application(app_id):
    try:
        application = ProfessionalApplication.query.get_or_404(app_id)
        db.session.delete(application)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Application deleted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error deleting application: {str(e)}'
        }), 500

# Client Requests Routes
@hmi_bp.route('/client-requests', methods=['POST'])
@cross_origin()
def submit_client_request():
    try:
        data = request.get_json()
        
        # Create new client request
        client_request = ClientRequest(
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            location=data.get('location'),
            make_location_public=data.get('makeLocationPublic', False),
            service_needs=data.get('serviceNeeds')
        )
        
        db.session.add(client_request)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Request submitted successfully!',
            'request': client_request.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error submitting request: {str(e)}'
        }), 500

@hmi_bp.route('/client-requests', methods=['GET'])
@cross_origin()
def get_client_requests():
    try:
        requests = ClientRequest.query.order_by(ClientRequest.submitted_at.desc()).all()
        return jsonify({
            'success': True,
            'requests': [req.to_dict() for req in requests]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching requests: {str(e)}'
        }), 500

@hmi_bp.route('/client-requests/<int:req_id>', methods=['DELETE'])
@cross_origin()
def delete_client_request(req_id):
    try:
        client_request = ClientRequest.query.get_or_404(req_id)
        db.session.delete(client_request)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Request deleted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error deleting request: {str(e)}'
        }), 500

# Contact Information Routes
@hmi_bp.route('/contact-info', methods=['GET'])
@cross_origin()
def get_contact_info():
    try:
        contact = ContactInfo.query.first()
        if not contact:
            # Create default contact info if none exists
            contact = ContactInfo(
                email='info@homemedcareintl.com',
                phone='+92 333-1234567',
                address='Office 1, ABC Plaza, Murree Road, Rawalpindi, Pakistan'
            )
            db.session.add(contact)
            db.session.commit()
        
        return jsonify({
            'success': True,
            'contactInfo': contact.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching contact info: {str(e)}'
        }), 500

@hmi_bp.route('/contact-info', methods=['PUT'])
@cross_origin()
def update_contact_info():
    try:
        data = request.get_json()
        
        contact = ContactInfo.query.first()
        if not contact:
            contact = ContactInfo()
            db.session.add(contact)
        
        contact.email = data.get('email', contact.email)
        contact.phone = data.get('phone', contact.phone)
        contact.address = data.get('address', contact.address)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Contact information updated successfully',
            'contactInfo': contact.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error updating contact info: {str(e)}'
        }), 500

# Reviews Routes
@hmi_bp.route('/reviews', methods=['POST'])
@cross_origin()
def submit_review():
    try:
        data = request.get_json()
        
        review = Review(
            professional_name=data.get('professionalName'),
            reviewer_name=data.get('reviewerName'),
            rating=data.get('rating'),
            comment=data.get('comment')
        )
        
        db.session.add(review)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Review submitted successfully',
            'review': review.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error submitting review: {str(e)}'
        }), 500

@hmi_bp.route('/reviews/<professional_name>', methods=['GET'])
@cross_origin()
def get_reviews_for_professional(professional_name):
    try:
        reviews = Review.query.filter_by(professional_name=professional_name).order_by(Review.submitted_at.desc()).all()
        return jsonify({
            'success': True,
            'reviews': [review.to_dict() for review in reviews]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching reviews: {str(e)}'
        }), 500

@hmi_bp.route('/reviews', methods=['GET'])
@cross_origin()
def get_all_reviews():
    try:
        reviews = Review.query.order_by(Review.submitted_at.desc()).all()
        return jsonify({
            'success': True,
            'reviews': [review.to_dict() for review in reviews]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching reviews: {str(e)}'
        }), 500

# Admin Authentication Route
@hmi_bp.route('/admin/login', methods=['POST'])
@cross_origin()
def admin_login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        # Simple authentication (in production, use proper password hashing)
        if username == 'admin' and password == 'hmi2024':
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'token': 'admin_token_123'  # In production, use JWT tokens
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid credentials'
            }), 401
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error during login: {str(e)}'
        }), 500

# Health check route
@hmi_bp.route('/health', methods=['GET'])
@cross_origin()
def health_check():
    return jsonify({
        'success': True,
        'message': 'HMI API is running',
        'status': 'healthy'
    }), 200

