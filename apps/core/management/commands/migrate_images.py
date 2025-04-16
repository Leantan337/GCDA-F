from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from wagtail.images.models import Image as WagtailImage
from apps.core.custom_image import CustomImage


class Command(BaseCommand):
    help = 'Migrates images from Wagtail default model to CustomImage model'

    def handle(self, *args, **options):
        self.stdout.write('Starting image migration...')
        
        # Get all images from default model
        wagtail_images = WagtailImage.objects.all()
        
        for image in wagtail_images:
            try:
                # Create new CustomImage instance
                custom_image = CustomImage(
                    title=image.title,
                    file=ContentFile(image.file.read(), name=image.filename),
                    width=image.width,
                    height=image.height,
                    created_at=image.created_at,
                    focal_point_x=image.focal_point_x,
                    focal_point_y=image.focal_point_y,
                    focal_point_width=image.focal_point_width,
                    focal_point_height=image.focal_point_height,
                    file_size=image.file_size,
                    collection=image.collection,
                )
                custom_image.save()
                
                # Copy tags
                custom_image.tags.set(image.tags.all())
                
                self.stdout.write(self.style.SUCCESS(f'Successfully migrated image: {image.title}'))
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Failed to migrate image {image.title}: {str(e)}')
                )
        
        self.stdout.write(self.style.SUCCESS('Image migration completed!'))
