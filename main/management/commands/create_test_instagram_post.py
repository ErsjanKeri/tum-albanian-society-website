from django.core.management.base import BaseCommand
from main.models import InstagramPost


class Command(BaseCommand):
    help = 'Create a test Instagram post for admin testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating test Instagram post...')
        
        # Create a test post
        test_post = InstagramPost.objects.create(
            caption="🎓 Welcome to Albanian Students TUM! Join our vibrant community of Albanian students at the Technical University of Munich. #AlbanianStudents #TUM #Munich #Community",
            post_url="https://www.instagram.com/p/test123/",
            post_type="image",
            primary_media_url="https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=400&h=400&fit=crop",
            media_urls=["https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=400&h=400&fit=crop"],
            display_order=0,
            is_active=True
        )
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created test Instagram post: {test_post}'))
        self.stdout.write(f'Post ID: {test_post.id}')
        self.stdout.write(f'Post URL: {test_post.post_url}')
        self.stdout.write(f'Caption: {test_post.caption[:50]}...')
        self.stdout.write(f'Media URLs: {len(test_post.get_all_media_urls())} images')
        
        self.stdout.write(self.style.SUCCESS('Test Instagram post created successfully!'))