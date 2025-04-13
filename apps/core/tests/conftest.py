try:
    import pytest
except ImportError:
    raise ImportError("pytest is required. Please install it using 'pip install pytest'")
from django.contrib.auth import get_user_model
from wagtail.models import Page, Site
from wagtail.test.utils import WagtailTestUtils
from wagtail_factories import PageFactory, SiteFactory

from apps.core.models import HomePage

@pytest.fixture
def admin_user():
    User = get_user_model()
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpassword'
    )

@pytest.fixture
def site_with_home():
    # Delete any existing sites and pages
    Site.objects.all().delete()
    Page.objects.all().delete()
    
    # Create a new homepage
    root = Page.objects.create(
        title='Root',
        slug='root',
        content_type_id=1,
        path='0001',
        depth=1,
        numchild=1,
        url_path='/',
    )
    
    home = HomePage.objects.create(
        title='Home',
        slug='home',
        content_type_id=1,
        path='00010001',
        depth=2,
        numchild=0,
        url_path='/home/',
        intro='Welcome to GCDA',
        about_title='About Us',
        about_description='We are a community development organization',
        services_title='Our Services',
        services_description='We provide various services',
        team_title='Our Team',
        team_description='Meet our dedicated team',
        parent=root
    )
    
    # Create a site with the new homepage
    site = Site.objects.create(
        hostname='localhost',
        root_page=home,
        is_default_site=True
    )
    
    return site

@pytest.fixture
def wagtail_test_utils():
    return WagtailTestUtils