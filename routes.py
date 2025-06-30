from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import app
from models import User, TrashPost
from datetime import datetime

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        user_type = request.form.get('user_type', 'user')
        
        # Validation
        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return render_template('register.html')
        
        if User.get_by_username(username):
            flash('Username already exists.', 'danger')
            return render_template('register.html')
        
        if User.get_by_email(email):
            flash('Email already registered.', 'danger')
            return render_template('register.html')
        
        # Create user
        user = User.create(username, email, password, user_type)
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Username and password are required.', 'danger')
            return render_template('login.html')
        
        user = User.get_by_username(username)
        if user and user.check_password(password):
            login_user(user)
            flash(f'Welcome back, {user.username}!', 'success')
            
            # Redirect based on user type
            if user.user_type == 'collector':
                return redirect(url_for('collector_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/user_dashboard')
@login_required
def user_dashboard():
    if current_user.user_type != 'user':
        flash('Access denied. This page is for users only.', 'danger')
        return redirect(url_for('collector_dashboard'))
    
    posts = TrashPost.get_by_user(current_user.id)
    total_earnings = sum(post.reward_points for post in posts if post.status == 'completed')
    
    return render_template('user_dashboard.html', posts=posts, total_earnings=total_earnings)

@app.route('/collector_dashboard')
@login_required
def collector_dashboard():
    if current_user.user_type != 'collector':
        flash('Access denied. This page is for collectors only.', 'danger')
        return redirect(url_for('user_dashboard'))
    
    available_posts = TrashPost.get_available()
    my_pickups = TrashPost.get_by_collector(current_user.id)
    
    return render_template('collector_dashboard.html', 
                         available_posts=available_posts, 
                         my_pickups=my_pickups)

@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    if current_user.user_type != 'user':
        flash('Only users can create trash posts.', 'danger')
        return redirect(url_for('collector_dashboard'))
    
    if request.method == 'POST':
        trash_type = request.form.get('trash_type')
        quantity = request.form.get('quantity')
        location = request.form.get('location')
        description = request.form.get('description')
        
        # Validation
        if not trash_type or not quantity or not location:
            flash('Trash type, quantity, and location are required.', 'danger')
            return render_template('create_post.html')
        
        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            flash('Quantity must be a positive number.', 'danger')
            return render_template('create_post.html')
        
        # Create post
        post = TrashPost.create(current_user.id, trash_type, quantity, location, description)
        flash('Trash post created successfully!', 'success')
        return redirect(url_for('user_dashboard'))
    
    return render_template('create_post.html')

@app.route('/post/<int:post_id>')
@login_required
def view_post(post_id):
    post = TrashPost.get(post_id)
    if not post:
        flash('Post not found.', 'danger')
        return redirect(url_for('user_dashboard' if current_user.user_type == 'user' else 'collector_dashboard'))
    
    # Get post owner information
    post_owner = User.get(post.user_id)
    collector = User.get(post.collector_id) if post.collector_id else None
    
    return render_template('view_post.html', post=post, post_owner=post_owner, collector=collector)

@app.route('/accept_pickup/<int:post_id>', methods=['POST'])
@login_required
def accept_pickup(post_id):
    if current_user.user_type != 'collector':
        flash('Only collectors can accept pickups.', 'danger')
        return redirect(url_for('user_dashboard'))
    
    post = TrashPost.get(post_id)
    if not post:
        flash('Post not found.', 'danger')
        return redirect(url_for('collector_dashboard'))
    
    if post.status != 'pending':
        flash('This pickup is no longer available.', 'warning')
        return redirect(url_for('collector_dashboard'))
    
    # Accept the pickup
    post.status = 'accepted'
    post.collector_id = current_user.id
    post.save()
    
    flash('Pickup accepted successfully!', 'success')
    return redirect(url_for('collector_dashboard'))

@app.route('/complete_pickup/<int:post_id>', methods=['POST'])
@login_required
def complete_pickup(post_id):
    if current_user.user_type != 'collector':
        flash('Only collectors can complete pickups.', 'danger')
        return redirect(url_for('user_dashboard'))
    
    post = TrashPost.get(post_id)
    if not post:
        flash('Post not found.', 'danger')
        return redirect(url_for('collector_dashboard'))
    
    if post.collector_id != current_user.id:
        flash('You can only complete your own pickups.', 'danger')
        return redirect(url_for('collector_dashboard'))
    
    if post.status != 'accepted':
        flash('This pickup cannot be completed.', 'warning')
        return redirect(url_for('collector_dashboard'))
    
    # Complete the pickup
    post.status = 'completed'
    post.completed_at = datetime.now()
    post.save()
    
    # Award points to the user
    user = User.get(post.user_id)
    if user:
        user.reward_points += post.reward_points
        user.save()
    
    flash('Pickup completed successfully! User has been awarded reward points.', 'success')
    return redirect(url_for('collector_dashboard'))

@app.route('/cancel_pickup/<int:post_id>', methods=['POST'])
@login_required
def cancel_pickup(post_id):
    post = TrashPost.get(post_id)
    if not post:
        flash('Post not found.', 'danger')
        return redirect(url_for('user_dashboard' if current_user.user_type == 'user' else 'collector_dashboard'))
    
    # Check permissions
    if current_user.user_type == 'user' and post.user_id != current_user.id:
        flash('You can only cancel your own posts.', 'danger')
        return redirect(url_for('user_dashboard'))
    
    if current_user.user_type == 'collector' and post.collector_id != current_user.id:
        flash('You can only cancel your own pickups.', 'danger')
        return redirect(url_for('collector_dashboard'))
    
    if post.status == 'completed':
        flash('Cannot cancel a completed pickup.', 'warning')
        return redirect(url_for('user_dashboard' if current_user.user_type == 'user' else 'collector_dashboard'))
    
    # Cancel the pickup
    post.status = 'pending'
    post.collector_id = None
    post.save()
    
    flash('Pickup cancelled successfully.', 'info')
    return redirect(url_for('user_dashboard' if current_user.user_type == 'user' else 'collector_dashboard'))
