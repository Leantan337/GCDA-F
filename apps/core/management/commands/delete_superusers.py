from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class Command(BaseCommand):
    help = 'Delete all superusers from the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force deletion without confirmation',
        )

    def handle(self, *args, **options):
        # Get all superusers
        superusers = User.objects.filter(Q(is_superuser=True))
        
        if not superusers.exists():
            self.stdout.write(self.style.WARNING('No superusers found in the database.'))
            return
        
        # Print all superusers that will be deleted
        self.stdout.write(self.style.WARNING('The following superusers will be deleted:'))
        for user in superusers:
            self.stdout.write(f"  - {user.username} (ID: {user.id})")
        
        # Check for --force flag
        if options['force']:
            self.delete_superusers(superusers)
            return
        
        # Confirm deletion
        self.stdout.write(self.style.WARNING('\nWARNING: This operation cannot be undone!'))
        confirm = input('Are you sure you want to delete all superusers? [y/N]: ')
        
        if confirm.lower() == 'y':
            self.delete_superusers(superusers)
        else:
            self.stdout.write(self.style.SUCCESS('Operation cancelled.'))
    
    def delete_superusers(self, superusers):
        count = superusers.count()
        # Store data for confirmation
        usernames = [user.username for user in superusers]
        
        # Delete all superusers
        superusers.delete()
        
        # Confirmation message
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} superuser(s):'))
        for username in usernames:
            self.stdout.write(f"  - {username}")
