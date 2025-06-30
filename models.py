from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    user_type = db.Column(db.String(20), default='user', nullable=False)  # 'user' or 'collector'
    reward_points = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to posts
    posts = db.relationship('TrashPost', foreign_keys='TrashPost.user_id', backref='owner', lazy='dynamic')
    collections = db.relationship('TrashPost', foreign_keys='TrashPost.collector_id', backref='collector', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
    
    @staticmethod
    def create(username, email, password, user_type='user'):
        user = User(username=username, email=email, user_type=user_type)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

class TrashPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    trash_type = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending', nullable=False)  # 'pending', 'accepted', 'completed'
    collector_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reward_points = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    def __init__(self, user_id, trash_type, quantity, location, description):
        self.user_id = user_id
        self.trash_type = trash_type
        self.quantity = quantity
        self.location = location
        self.description = description
        self.reward_points = self.calculate_reward_points()
    
    def calculate_reward_points(self):
        # Simple reward calculation based on trash type and quantity
        base_points = {
            'plastic': 2,
            'glass': 3,
            'metal': 4,
            'paper': 1,
            'electronic': 5,
            'organic': 1
        }
        return base_points.get(self.trash_type, 1) * self.quantity
    
    @staticmethod
    def get_available():
        return TrashPost.query.filter_by(status='pending').order_by(TrashPost.created_at.desc()).all()
    
    @staticmethod
    def create(user_id, trash_type, quantity, location, description):
        post = TrashPost(user_id, trash_type, quantity, location, description)
        db.session.add(post)
        db.session.commit()
        return post
