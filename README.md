# Green Community Development Association (GCDA) Website Documentation

## Project Overview
The GCDA website is a comprehensive Django-based NGO website using Wagtail CMS. It serves as the digital platform for the Green Community Development Association, focusing on community development, environmental sustainability, and social impact in Sudan.

### Mission and Vision
- **Mission**: To empower local communities through sustainable development initiatives
- **Vision**: Creating self-sufficient, environmentally conscious communities
- **Location**: Tenedba Camp, Al Gedarif, Sudan

## Technical Stack

### Backend
- **Framework**: Django 5.1.6
  - URL routing
  - Model-View-Template (MVT) architecture
  - ORM for database operations
- **CMS**: Wagtail
  - Page tree management
  - Image management
  - Document handling
  - Rich text editing
- **Database**: SQLite3 (Development)
  - Easy setup
  - No configuration needed
  - Suitable for development

### Authentication 
- Django Allauth
  - Email authentication (Completed)
    - Login page styled 
    - Signup page styled 
    - Email verification page styled 
  - Custom user model implemented 
  - Rate limiting configured 
  - Password reset functionality 

### Frontend
- **Framework**: Bootstrap 5
  - Responsive grid system implemented 
  - Mobile-first design
  - Custom components
    - Authentication pages styled 
    - Homepage sections (In Progress)
    - Navigation (In Progress)
- **JavaScript Libraries**:
  - AOS (Animate On Scroll)
  - Swiper for carousels
  - GLightbox for image popups
  - Custom JavaScript for interactions

### Forms 
- Crispy Forms
  - Bootstrap 5 integration completed 
  - Form layouts styled 
  - Field customization implemented 

## Project Structure

### Directory Layout
```
GCDA-F/
├── apps/
│   ├── core/         # Homepage, about, contact, etc.
│   ├── news/         # News section (Wagtail-based)
│   ├── donations/    # Donation functionality
│   ├── engagement/   # Community engagement
│   └── comments/     # User comments
├── accounts/         # Custom user model & authentication
├── static/           # Static assets (CSS, JS, images)
├── templates/        # HTML templates (Django + Wagtail)
├── config/           # Django settings & configuration
├── manage.py         # Django entrypoint
└── requirements.txt  # Python dependencies
```

## Progress Overview (April 2025)

### Completed Features
- Authentication system with custom user model, registration, login, logout, email verification, and password reset
- Modern, responsive UI for all authentication and profile pages
- News section with:
  - Wagtail-powered news articles
  - Featured images and categories
  - Modern news list and detail pages
  - AJAX-powered "Load More" for news list
- Form layouts (Crispy Forms + Bootstrap 5)
- Static and media file handling

### In Progress
- Homepage hero and section content
- Navigation and header/footer includes
- Sidebar features for news (search, recent posts, categories)
- Donation and engagement modules

### Pending
- Dynamic event management
- Community features (forums, user groups)
- Advanced search and filtering
- Additional content pages

## Credits
- **Template Base**: BizLand by BootstrapMade ([link](https://bootstrapmade.com/bizland-bootstrap-business-template/))
- **License**: [BootstrapMade License](https://bootstrapmade.com/license/)

## Features

### 1. Content Management System
- **Wagtail Admin Interface**
  - URL: `/admin/`
  - Features:
    - Page management
    - Media library
    - User management
    - Settings

### 2. Homepage Sections
- **Hero Section**
  - Welcome message
  - Call-to-action buttons
  - Background video/image
  
- **About Section**
  - Mission statement
  - Organization history
  - Key achievements
  
- **Services Section**
  - Community development
  - Environmental projects
  - Education programs
  
- **Team Section**
  - Team member profiles
  - Social media links
  - Role descriptions
  
- **Contact Section**
  - Contact form
  - Location map
  - Contact details

### 3. Interactive Elements
- **Animations**
  - Scroll animations (AOS)
  - Hover effects
  - Smooth scrolling
  
- **Forms**
  - Contact form
  - Newsletter signup
  - Validation
  
- **Media**
  - Image galleries
  - Video integration
  - Document downloads

## Setup and Installation

### 1. Prerequisites
- Python 3.13.2
- pip (Python package manager)
- Git
- Virtual environment

### 2. Environment Setup
```bash
# Clone repository
git clone <repository-url>
cd GCDA

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration
```python
# settings.py
INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    # ...
    
    # Wagtail apps
    'wagtail.core',
    # ...
    
    # Third-party apps
    'allauth',
    'crispy_forms',
    
    # Local apps
    'apps.core',
    'apps.donations',
    'apps.news',
    'apps.engagement',
]
```

### 4. Database Setup
```bash
# Create database tables
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic
```

## Content Management Guide

### 1. Creating Pages
1. Access Wagtail Admin
2. Navigate to Pages
3. Click "Add Child Page"
4. Select page type
5. Fill in content
6. Preview and publish

### 2. Managing Media
- **Images**
  - Supported formats: JPG, PNG, GIF
  - Automatic resizing
  - Alt text support
  
- **Documents**
  - PDF, DOC, DOCX support
  - Version control
  - Search indexing

### 3. SEO Management
- Meta titles
- Meta descriptions
- OG tags
- Sitemap generation

## Development Guidelines

### 1. Code Style
- Follow PEP 8
- Use meaningful variable names
- Document functions and classes
- Keep functions small and focused

### 2. Git Workflow
- Feature branches
- Meaningful commit messages
- Pull request reviews
- Version tagging

### 3. Testing
```bash
# Run tests
python manage.py test

# Coverage report
coverage run manage.py test
coverage report
```

## Deployment

### 1. Production Setup
- Set DEBUG=False
- Configure ALLOWED_HOSTS
- Set secure cookies
- Enable HTTPS

### 2. Server Requirements
- Ubuntu 20.04 LTS
- Nginx
- Gunicorn
- PostgreSQL
- Redis (optional)

### 3. Maintenance
- Regular backups
- Security updates
- Performance monitoring
- Error tracking

## Security Measures

### 1. Django Security
- CSRF protection
- XSS prevention
- SQL injection protection
- Password hashing

### 2. Server Security
- Firewall configuration
- SSL/TLS setup
- Regular updates
- Access logging

## Performance Optimization

### 1. Caching
- Template caching
- Database query optimization
- Static file serving
- Media file optimization

### 2. Load Time
- Image compression
- CSS/JS minification
- Lazy loading
- Browser caching

## Internationalization

### 1. Language Support
- English (default)
- French
- Spanish
- Arabic

### 2. Translation Process
```bash
# Generate message files
python manage.py makemessages -l fr

# Compile messages
python manage.py compilemessages
```

## API Documentation

### 1. Available Endpoints
- `/api/pages/` - Page data
- `/api/media/` - Media files
- `/api/forms/` - Form submissions

### 2. Authentication
- Token-based auth
- API key management
- Rate limiting

## Troubleshooting

### Common Issues
1. Template errors
2. Static files not loading
3. Database migrations
4. Permission issues

### Solutions
- Check template paths
- Run collectstatic
- Review migration files
- Check file permissions

## Future Roadmap

### Phase 1 (Q2 2025)
- Online donation system
- Event management
- Member portal

### Phase 2 (Q3 2025)
- Mobile app
- API expansion
- Analytics dashboard

### Phase 3 (Q4 2025)
- AI-powered chatbot
- Advanced reporting
- Community forum

## Support and Resources

### Documentation
- [Django Docs](https://docs.djangoproject.com/)
- [Wagtail Docs](https://docs.wagtail.org/)
- [Bootstrap Docs](https://getbootstrap.com/docs/)

### Community
- GitHub Issues
- Stack Overflow
- Discord channel

## Team

### Core Team
- Hyab Welay (CEO & Founder)
- Development Team
- Full Stack developer by
  - Natnael Zeru 
  - Content Team
  - Design Team

### Contributors
- Community contributors
- Open source maintainers

## License and Legal

### License
All rights reserved GCDA

### Privacy Policy
- Data collection
- User rights
- GDPR compliance

### Terms of Service
- Usage terms
- Content rights
- Liability limitations
