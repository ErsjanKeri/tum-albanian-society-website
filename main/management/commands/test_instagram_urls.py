from django.core.management.base import BaseCommand
from main.forms import InstagramPostAdminForm
from main.models import InstagramPost


class Command(BaseCommand):
    help = 'Test Instagram CDN URL parsing'

    def handle(self, *args, **options):
        self.stdout.write('Testing Instagram CDN URL parsing...')
        
        # Your concatenated Instagram URLs
        test_urls = "https://scontent-muc2-1.cdninstagram.com/v/t51.2885-15/535663097_17942113797044933_5429181605157322643_n.jpg?stp=dst-jpegr_e35_p1080x1080_tt6&efg=eyJ2ZW5jb2RlX3RhZyI6IkNBUk9VU0VMX0lURU0uaW1hZ2VfdXJsZ2VuLjE0NDB4MTUxNy5oZHIuZjgyNzg3LmRlZmF1bHRfaW1hZ2UuYzIifQ&_nc_ht=scontent-muc2-1.cdninstagram.com&_nc_cat=105&_nc_oc=Q6cZ2QGMylM2LnaST1qrgrDw2A4B9aPMSjXYVqGfE2zk4cH2csD9-L-lCgfpz6W3IQIE3TYQ8u7HK9W_nNad3b6cqF41&_nc_ohc=HtDKXMJj9moQ7kNvwG4QFUM&_nc_gid=uU0VYkht46PhwNyF9h-R6g&edm=AP4sbd4BAAAA&ccb=7-5&ig_cache_key=MzcwMjY0NDExNjYzNDgyMDU1NQ%3D%3D.3-ccb7-5&oh=00_Afah2nWoZD5wktQcFZSR_WPbKTWXx7d5ihGScFPRT5Jj3g&oe=68BDCC38&_nc_sid=7a9f4bhttps://scontent-muc2-1.cdninstagram.com/v/t51.2885-15/536322559_17942113827044933_587183942813015664_n.jpg?stp=dst-jpegr_e35_p1080x1080_tt6&efg=eyJ2ZW5jb2RlX3RhZyI6IkNBUk9VU0VMX0lURU0uaW1hZ2VfdXJsZ2VuLjE0NDB4MTkyMC5oZHIuZjgyNzg3LmRlZmF1bHRfaW1hZ2UuYzIifQ&_nc_ht=scontent-muc2-1.cdninstagram.com&_nc_cat=105&_nc_oc=Q6cZ2QGMylM2LnaST1qrgrDw2A4B9aPMSjXYVqGfE2zk4cH2csD9-L-lCgfpz6W3IQIE3TYQ8u7HK9W_nNad3b6cqF41&_nc_ohc=6AqIKVnOl-0Q7kNvwEOVzeW&_nc_gid=uU0VYkht46PhwNyF9h-R6g&edm=AP4sbd4BAAAA&ccb=7-5&ig_cache_key=MzcwMjY0NDExNjYyNjQ0NDA2NQ%3D%3D.3-ccb7-5&oh=00_AfZAAwmztKYEU8b2SPDr-Gv02n9r1Bb2qel5n8pvbjYGhA&oe=68BDCBF3&_nc_sid=7a9f4b"
        
        # Test the form parsing
        import uuid
        unique_id = str(uuid.uuid4())[:8]
        form_data = {
            'post_url': f'https://www.instagram.com/p/test{unique_id}/',
            'caption': 'Test post with Instagram CDN images',
            'post_type': 'carousel',
            'media_urls_text': test_urls,
            'display_order': 0,
            'is_active': True
        }
        
        form = InstagramPostAdminForm(data=form_data)
        
        if form.is_valid():
            self.stdout.write(self.style.SUCCESS('✓ Form validation passed'))
            
            # Check the parsed URLs
            parsed_urls = form.cleaned_data.get('media_urls_text', [])
            self.stdout.write(f'✓ Parsed {len(parsed_urls)} URLs:')
            
            for i, url in enumerate(parsed_urls, 1):
                self.stdout.write(f'  {i}. {url[:100]}...')
                
                # Test if the URL is considered valid
                from main.models import ImageURLField
                field = ImageURLField()
                try:
                    if field.is_valid_image_url(url):
                        self.stdout.write(self.style.SUCCESS(f'     ✓ URL {i} is valid'))
                    else:
                        self.stdout.write(self.style.WARNING(f'     ⚠ URL {i} validation failed'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'     ✗ URL {i} error: {e}'))
            
            # Try to save the post
            try:
                post = form.save()
                self.stdout.write(self.style.SUCCESS(f'✓ Successfully created post: {post}'))
                self.stdout.write(f'  - Media count: {post.get_media_count()}')
                self.stdout.write(f'  - Post type: {post.post_type}')
                self.stdout.write(f'  - Primary URL: {post.primary_media_url[:50]}...')
                
                # Clean up
                post.delete()
                self.stdout.write('✓ Cleaned up test post')
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Failed to save post: {e}'))
        else:
            self.stdout.write(self.style.ERROR('✗ Form validation failed:'))
            for field, errors in form.errors.items():
                self.stdout.write(f'  {field}: {errors}')
        
        self.stdout.write(self.style.SUCCESS('Instagram URL parsing test completed!'))