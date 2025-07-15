from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class ProfessionalApplication(db.Model):
    __tablename__ = 'professional_applications'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    profile_picture = db.Column(db.String(255), nullable=True)  # Store filename
    gender = db.Column(db.String(10), nullable=True)
    cv_details = db.Column(db.Text, nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    
    def to_dict(self):
        return {
            'id': self.id,
            'fullName': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'location': self.location,
            'specialty': self.specialty,
            'profilePicture': self.profile_picture,
            'gender': self.gender,
            'cvDetails': self.cv_details,
            'submittedAt': self.submitted_at.isoformat(),
            'status': self.status
        }

class ClientRequest(db.Model):
    __tablename__ = 'client_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    make_location_public = db.Column(db.Boolean, default=False)
    service_needs = db.Column(db.Text, nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, completed
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'location': self.location,
            'makeLocationPublic': self.make_location_public,
            'serviceNeeds': self.service_needs,
            'submittedAt': self.submitted_at.isoformat(),
            'status': self.status
        }

class ContactInfo(db.Model):
    __tablename__ = 'contact_info'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'updatedAt': self.updated_at.isoformat()
        }

class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    professional_name = db.Column(db.String(100), nullable=False)
    reviewer_name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text, nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'professionalName': self.professional_name,
            'reviewerName': self.reviewer_name,
            'rating': self.rating,
            'comment': self.comment,
            'date': self.submitted_at.strftime('%Y-%m-%d')
        }

