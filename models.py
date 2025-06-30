from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import app_data
from datetime import datetime

class User(UserMixin):
    def __init__(self, id, username, email, password_hash, user_type='user', reward_points=0):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.user_type = user_type  # 'user' or 'collector'
        self.reward_points = reward_points
        self.created_at = datetime.now()
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def save(self):
        app_data['users'][self.id] = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password_hash': self.password_hash,
            'user_type': self.user_type,
            'reward_points': self.reward_points,
            'created_at': self.created_at
        }
    
    @staticmethod
    def get(user_id):
        user_data = app_data['users'].get(user_id)
        if user_data:
            return User(
                user_data['id'],
                user_data['username'],
                user_data['email'],
                user_data['password_hash'],
                user_data['user_type'],
                user_data['reward_points']
            )
        return None
    
    @staticmethod
    def get_by_username(username):
        for user_data in app_data['users'].values():
            if user_data['username'] == username:
                return User(
                    user_data['id'],
                    user_data['username'],
                    user_data['email'],
                    user_data['password_hash'],
                    user_data['user_type'],
                    user_data['reward_points']
                )
        return None
    
    @staticmethod
    def get_by_email(email):
        for user_data in app_data['users'].values():
            if user_data['email'] == email:
                return User(
                    user_data['id'],
                    user_data['username'],
                    user_data['email'],
                    user_data['password_hash'],
                    user_data['user_type'],
                    user_data['reward_points']
                )
        return None
    
    @staticmethod
    def create(username, email, password, user_type='user'):
        user_id = app_data['next_user_id']
        app_data['next_user_id'] += 1
        
        user = User(user_id, username, email, '', user_type)
        user.set_password(password)
        user.save()
        return user

class TrashPost:
    def __init__(self, id, user_id, trash_type, quantity, location, description, status='pending'):
        self.id = id
        self.user_id = user_id
        self.trash_type = trash_type
        self.quantity = quantity
        self.location = location
        self.description = description
        self.status = status  # 'pending', 'accepted', 'completed'
        self.collector_id = None
        self.reward_points = self.calculate_reward_points()
        self.created_at = datetime.now()
        self.completed_at = None
    
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
    
    def save(self):
        app_data['posts'][self.id] = {
            'id': self.id,
            'user_id': self.user_id,
            'trash_type': self.trash_type,
            'quantity': self.quantity,
            'location': self.location,
            'description': self.description,
            'status': self.status,
            'collector_id': self.collector_id,
            'reward_points': self.reward_points,
            'created_at': self.created_at,
            'completed_at': self.completed_at
        }
    
    @staticmethod
    def get(post_id):
        post_data = app_data['posts'].get(post_id)
        if post_data:
            post = TrashPost(
                post_data['id'],
                post_data['user_id'],
                post_data['trash_type'],
                post_data['quantity'],
                post_data['location'],
                post_data['description'],
                post_data['status']
            )
            post.collector_id = post_data['collector_id']
            post.reward_points = post_data['reward_points']
            post.created_at = post_data['created_at']
            post.completed_at = post_data['completed_at']
            return post
        return None
    
    @staticmethod
    def get_by_user(user_id):
        posts = []
        for post_data in app_data['posts'].values():
            if post_data['user_id'] == user_id:
                post = TrashPost(
                    post_data['id'],
                    post_data['user_id'],
                    post_data['trash_type'],
                    post_data['quantity'],
                    post_data['location'],
                    post_data['description'],
                    post_data['status']
                )
                post.collector_id = post_data['collector_id']
                post.reward_points = post_data['reward_points']
                post.created_at = post_data['created_at']
                post.completed_at = post_data['completed_at']
                posts.append(post)
        return sorted(posts, key=lambda x: x.created_at, reverse=True)
    
    @staticmethod
    def get_by_collector(collector_id):
        posts = []
        for post_data in app_data['posts'].values():
            if post_data['collector_id'] == collector_id:
                post = TrashPost(
                    post_data['id'],
                    post_data['user_id'],
                    post_data['trash_type'],
                    post_data['quantity'],
                    post_data['location'],
                    post_data['description'],
                    post_data['status']
                )
                post.collector_id = post_data['collector_id']
                post.reward_points = post_data['reward_points']
                post.created_at = post_data['created_at']
                post.completed_at = post_data['completed_at']
                posts.append(post)
        return sorted(posts, key=lambda x: x.created_at, reverse=True)
    
    @staticmethod
    def get_available():
        posts = []
        for post_data in app_data['posts'].values():
            if post_data['status'] == 'pending':
                post = TrashPost(
                    post_data['id'],
                    post_data['user_id'],
                    post_data['trash_type'],
                    post_data['quantity'],
                    post_data['location'],
                    post_data['description'],
                    post_data['status']
                )
                post.collector_id = post_data['collector_id']
                post.reward_points = post_data['reward_points']
                post.created_at = post_data['created_at']
                post.completed_at = post_data['completed_at']
                posts.append(post)
        return sorted(posts, key=lambda x: x.created_at, reverse=True)
    
    @staticmethod
    def create(user_id, trash_type, quantity, location, description):
        post_id = app_data['next_post_id']
        app_data['next_post_id'] += 1
        
        post = TrashPost(post_id, user_id, trash_type, quantity, location, description)
        post.save()
        return post
