from django.core.management.base import BaseCommand
from main.models import InstagramPost, InstagramConfig
from main.forms import InstagramPostAdminForm


class Command(BaseCommand):
    help = 'Test Instagram admin functionality'

    def handle(self, *args, **options):
        self.stdout.write('Testing Instagram admin functionality...')
        
        # Test 1: Create Instagram config if it doesn't exist
        config, created = InstagramConfig.objects.get_or_create(
            defaults={
                'posts_per_page': 6,
                'show_captions': True,
                'max_caption_length': 2000,
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Created Instagram config'))
        else:
            self.stdout.write('✓ Instagram config already exists')
        
        # Test 2: Test form initialization
        try:
            form = InstagramPostAdminForm()
            self.stdout.write(self.style.SUCCESS('✓ Admin form initializes correctly'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Admin form initialization failed: {e}'))
            return
        
        # Test 3: Test form with sample data
        sample_data = {
            'post_url': 'https://www.instagram.com/p/test123/',
            'caption': 'Test Instagram post',
            'post_type': 'image',
            'primary_media_url': 'https://example.com/test.jpg',
            'media_urls_text': 'https://example.com/test.jpg',
            'display_order': 0,
            'is_active': True
        }
        
        try:
            form = InstagramPostAdminForm(data=sample_data)
            if form.is_valid():
                self.stdout.write(self.style.SUCCESS('✓ Admin form validates correctly'))
                
                # Test saving
                post = form.save()
                self.stdout.write(self.style.SUCCESS(f'✓ Created test post: {post}'))
                
                # Clean up
                post.delete()
                self.stdout.write('✓ Cleaned up test post')
                
            else:
                self.stdout.write(self.style.WARNING(f'⚠ Form validation issues: {form.errors}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Form validation failed: {e}'))
        
        # Test 4: Check URL patterns
        try:
            from django.urls import reverse
            
            # Test quick add URL
            quick_add_url = reverse('instagram_quick_add')
            self.stdout.write(self.style.SUCCESS(f'✓ Quick add URL resolved: {quick_add_url}'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ URL resolution failed: {e}'))
        
        self.stdout.write(self.style.SUCCESS('Instagram admin functionality test completed!'))