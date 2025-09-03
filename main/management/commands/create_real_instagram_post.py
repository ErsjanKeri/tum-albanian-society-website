from django.core.management.base import BaseCommand
from main.models import InstagramPost


class Command(BaseCommand):
    help = 'Create a real Instagram post with your CDN URLs'

    def handle(self, *args, **options):
        self.stdout.write('Creating real Instagram post with your CDN URLs...')
        
        # Your properly separated Instagram CDN URLs
        url1 = "https://scontent-muc2-1.cdninstagram.com/v/t51.2885-15/535663097_17942113797044933_5429181605157322643_n.jpg?stp=dst-jpegr_e35_p1080x1080_tt6&efg=eyJ2ZW5jb2RlX3RhZyI6IkNBUk9VU0VMX0lURU0uaW1hZ2VfdXJsZ2VuLjE0NDB4MTUxNy5oZHIuZjgyNzg3LmRlZmF1bHRfaW1hZ2UuYzIifQ&_nc_ht=scontent-muc2-1.cdninstagram.com&_nc_cat=105&_nc_oc=Q6cZ2QGMylM2LnaST1qrgrDw2A4B9aPMSjXYVqGfE2zk4cH2csD9-L-lCgfpz6W3IQIE3TYQ8u7HK9W_nNad3b6cqF41&_nc_ohc=HtDKXMJj9moQ7kNvwG4QFUM&_nc_gid=uU0VYkht46PhwNyF9h-R6g&edm=AP4sbd4BAAAA&ccb=7-5&ig_cache_key=MzcwMjY0NDExNjYzNDgyMDU1NQ%3D%3D.3-ccb7-5&oh=00_Afah2nWoZD5wktQcFZSR_WPbKTWXx7d5ihGScFPRT5Jj3g&oe=68BDCC38&_nc_sid=7a9f4b"
        
        url2 = "https://scontent-muc2-1.cdninstagram.com/v/t51.2885-15/536322559_17942113827044933_587183942813015664_n.jpg?stp=dst-jpegr_e35_p1080x1080_tt6&efg=eyJ2ZW5jb2RlX3RhZyI6IkNBUk9VU0VMX0lURU0uaW1hZ2VfdXJsZ2VuLjE0NDB4MTkyMC5oZHIuZjgyNzg3LmRlZmF1bHRfaW1hZ2UuYzIifQ&_nc_ht=scontent-muc2-1.cdninstagram.com&_nc_cat=105&_nc_oc=Q6cZ2QGMylM2LnaST1qrgrDw2A4B9aPMSjXYVqGfE2zk4cH2csD9-L-lCgfpz6W3IQIE3TYQ8u7HK9W_nNad3b6cqF41&_nc_ohc=6AqIKVnOl-0Q7kNvwEOVzeW&_nc_gid=uU0VYkht46PhwNyF9h-R6g&edm=AP4sbd4BAAAA&ccb=7-5&ig_cache_key=MzcwMjY0NDExNjYyNjQ0NDA2NQ%3D%3D.3-ccb7-5&oh=00_AfZAAwmztKYEU8b2SPDr-Gv02n9r1Bb2qel5n8pvbjYGhA&oe=68BDCBF3&_nc_sid=7a9f4b"
        
        # Create the post
        post = InstagramPost.objects.create(
            caption="🎓 Albanian Students TUM - Join our community! 🇦🇱 #AlbanianStudents #TUM #Munich #University #Community #Albania",
            post_url="https://www.instagram.com/p/real_post_example/",
            post_type="carousel",
            primary_media_url=url1,
            media_urls=[url1, url2],
            display_order=0,
            is_active=True
        )
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created Instagram post: {post}'))
        self.stdout.write(f'  - Post ID: {post.id}')
        self.stdout.write(f'  - Post type: {post.post_type}')
        self.stdout.write(f'  - Media count: {post.get_media_count()}')
        self.stdout.write(f'  - Primary URL: {post.primary_media_url[:80]}...')
        self.stdout.write(f'  - All URLs: {len(post.get_all_media_urls())} total')
        
        # Test URL accessibility
        self.stdout.write('\nTesting URL accessibility...')
        import requests
        
        for i, url in enumerate(post.get_all_media_urls(), 1):
            try:
                response = requests.head(url, timeout=10)
                if response.status_code == 200:
                    self.stdout.write(self.style.SUCCESS(f'  ✓ URL {i}: Accessible (Status: {response.status_code})'))
                else:
                    self.stdout.write(self.style.WARNING(f'  ⚠ URL {i}: Status {response.status_code}'))
            except requests.exceptions.RequestException as e:
                self.stdout.write(self.style.ERROR(f'  ✗ URL {i}: Error - {e}'))
        
        self.stdout.write(self.style.SUCCESS('\nReal Instagram post created successfully!'))
        self.stdout.write(f'You can now view this post on your website or test it in the admin interface.')
        self.stdout.write(f'Post ID: {post.id}')