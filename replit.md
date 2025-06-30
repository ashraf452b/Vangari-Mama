# ScrapMama - Trash Collection Marketplace

## Overview

ScrapMama is a Flask-based web application that serves as a marketplace connecting waste generators with collectors. The platform allows users to post their trash for collection while earning reward points, and enables collectors to find and manage pickup opportunities. The application promotes environmental sustainability by facilitating efficient waste collection and recycling.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Flask
- **UI Framework**: Bootstrap 5 with dark theme support
- **Icons**: Font Awesome 6.0
- **JavaScript**: Vanilla JavaScript for enhanced user interactions
- **Responsive Design**: Mobile-first approach using Bootstrap grid system

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Authentication**: Flask-Login for session management
- **Password Security**: Werkzeug for password hashing
- **Data Storage**: In-memory storage using Python dictionaries
- **Session Management**: Flask sessions with configurable secret key

### Application Structure
```
/
├── app.py              # Application factory and configuration
├── main.py             # Application entry point
├── models.py           # Data models (User, TrashPost)
├── routes.py           # URL routes and view functions
├── templates/          # Jinja2 HTML templates
│   ├── base.html       # Base template with navigation
│   ├── index.html      # Landing page
│   ├── login.html      # Authentication forms
│   ├── register.html   # User registration
│   ├── user_dashboard.html     # User interface
│   ├── collector_dashboard.html # Collector interface
│   ├── create_post.html        # Trash posting form
│   └── view_post.html         # Post details view
└── static/
    ├── css/custom.css  # Custom styling
    └── js/main.js      # Client-side functionality
```

## Key Components

### User Management System
- **Two User Types**: Regular users (waste generators) and collectors
- **Authentication**: Username/password with secure hashing
- **Session Management**: Flask-Login integration for persistent sessions
- **Reward System**: Point-based rewards for completed transactions

### Trash Post Management
- **Post Creation**: Users can create posts with trash type, quantity, location, and description
- **Status Tracking**: Posts progress through pending → accepted → completed states
- **Categorization**: Support for multiple trash types (plastic, glass, metal, paper, electronic, organic)
- **Location-Based**: Address-based pickup coordination

### Dashboard Systems
- **User Dashboard**: View posts, track earnings, manage account
- **Collector Dashboard**: Find available pickups, manage accepted jobs
- **Real-time Updates**: Auto-refresh functionality for collectors

## Data Flow

### User Registration & Authentication
1. User submits registration form with user type selection
2. System validates uniqueness of username/email
3. Password is hashed and stored securely
4. User can log in and access appropriate dashboard

### Trash Collection Workflow
1. User creates trash post with details and location
2. Post appears in collector dashboard as available pickup
3. Collector accepts the post (status: pending → accepted)
4. Collector completes pickup (status: accepted → completed)
5. User receives reward points based on trash type and quantity

### Data Storage Structure
```python
app_data = {
    'users': {user_id: user_data},      # User profiles and authentication
    'posts': {post_id: post_data},      # Trash collection posts
    'next_user_id': int,                # Auto-incrementing ID counter
    'next_post_id': int                 # Auto-incrementing ID counter
}
```

## External Dependencies

### Frontend Dependencies
- **Bootstrap 5**: UI framework and components (CDN)
- **Font Awesome 6**: Icon library (CDN)
- **Custom CSS**: Application-specific styling

### Backend Dependencies
- **Flask**: Core web framework
- **Flask-Login**: User session management
- **Werkzeug**: Password hashing and WSGI utilities

### Browser Requirements
- Modern browsers supporting ES6+ JavaScript
- Bootstrap 5 compatibility
- Dark theme support (preferred)

## Deployment Strategy

### Current Configuration
- **Development Mode**: Debug enabled, in-memory storage
- **Host Configuration**: 0.0.0.0:5000 for external access
- **Proxy Support**: ProxyFix middleware for reverse proxy compatibility
- **Environment Variables**: SESSION_SECRET for production security

### Production Considerations
- **Database Migration**: Current in-memory storage needs persistent database
- **Session Security**: Environment-based secret key configuration
- **Static Assets**: CDN delivery for Bootstrap and Font Awesome
- **Auto-refresh**: 30-second intervals for collector dashboard updates

### Scaling Recommendations
- **Database**: Implement PostgreSQL or similar for data persistence
- **Caching**: Redis for session storage and frequently accessed data
- **File Storage**: Cloud storage for potential image uploads
- **Load Balancing**: Support for multiple Flask instances

## Changelog
- June 30, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.