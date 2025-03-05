from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from wagtail.models import Site, Page
from core.models import HomePage

class Command(BaseCommand):
    help = 'Sets up the initial homepage'

    def handle(self, *args, **options):
        # Delete any existing sites and pages
        Site.objects.all().delete()
        Page.objects.all().delete()

        # Create a new root page
        root_content_type = ContentType.objects.get_for_model(Page)
        root_page = Page(
            title="Root",
            slug='root',
            content_type=root_content_type,
            path='0001',
            depth=1,
            numchild=0,
            url_path='/',
        )
        root_page.save()

        # Get content type for homepage
        homepage_content_type = ContentType.objects.get_for_model(HomePage)

        # Create a new homepage
        homepage = HomePage(
            title="Green Community Development Association",
            draft_title="Green Community Development Association",
            slug='home',
            content_type=homepage_content_type,
            show_in_menus=True,
            # Hero Section
            mission_statement="Empowering communities through sustainable development",
            hero_subtitle="Creating positive change in Sudan",
            hero_cta_text="Join Us Today",
            hero_video_url="",
            # About Section
            about_title="About GCDA",
            about_subtitle="Our Mission & Vision",
            about_description="We are dedicated to sustainable development and community empowerment in Sudan.",
            about_content_secondary="Through education, sustainable practices, and community engagement, we build a better future.",
            about_cta_text="Learn More",
            about_cta_link="http://localhost:8000/about/",
            # Services Section
            services_title="Our Services",
            services_subtitle="What We Do",
            services_description="We provide various services to help communities thrive and grow sustainably.",
            # Team Section
            team_title="Our Team",
            team_subtitle="Meet Our Experts",
            team_description="Our dedicated team of professionals working towards positive change.",
            # Contact Section
            contact_title="Contact Us",
            contact_subtitle="Get in Touch",
            contact_description="We'd love to hear from you. Reach out to us for any inquiries or collaborations.",
            address="Khartoum, Sudan",
            email="contact@gcda.org",
            phone="+249 123 456 789",
            # Stats
            people_helped=1000,
            countries_served=5,
            projects_completed=50,
            volunteers=100,
            # Tree fields
            path='00010001',
            depth=2,
            numchild=0,
            url_path='/home/',
        )

        root_page.add_child(instance=homepage)

        # Create a site with the new homepage set as the root
        Site.objects.create(
            hostname='localhost',
            root_page=homepage,
            is_default_site=True,
            site_name='GCDA'
        )

        self.stdout.write(self.style.SUCCESS('Successfully set up homepage'))
