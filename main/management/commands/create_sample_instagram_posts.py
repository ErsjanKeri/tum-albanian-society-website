from django.core.management.base import BaseCommand
from main.models import InstagramPost


class Command(BaseCommand):
    help = 'Create sample Instagram posts for testing the management interface'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=3,
            help='Number of sample posts to create'
        )

    def handle(self, *args, **options):
        count = options['count']
        
        sample_posts = [
            {
                'post_url': 'https://www.instagram.com/p/ABC123/',
                'caption': 'Welcome to our Albanian Students community at TUM! 🇦🇱 Join us for amazing events and networking opportunities.',
                'post_type': 'image',
                'primary_media_url': 'https://via.placeholder.com/600x600/C13584/FFFFFF?text=Sample+Post+1',
                'display_order': 1,
                'is_active': True
            },
            {
                'post_url': 'https://www.instagram.com/p/DEF456/',
                'caption': 'Our latest hackathon was incredible! Thanks to everyone who participated. 💻✨ #TUMHackathon #AlbanianStudents',
                'post_type': 'carousel',
                'primary_media_url': 'https://via.placeholder.com/600x600/E6683C/FFFFFF?text=Hackathon+Main',
                'media_urls': [
                    'https://via.placeholder.com/600x600/E6683C/FFFFFF?text=Hackathon+Main',
                    'https://via.placeholder.com/600x600/DC2743/FFFFFF?text=Team+Work',
                    'https://via.placeholder.com/600x600/CC2366/FFFFFF?text=Winners'
                ],
                'display_order': 2,
                'is_active': True
            },
            {
                'post_url': 'https://www.instagram.com/p/GHI789/',
                'caption': 'Study session at TUM library! 📚 Great atmosphere for learning together.',
                'post_type': 'image',
                'primary_media_url': 'https://via.placeholder.com/600x600/BC1888/FFFFFF?text=Study+Session',
                'display_order': 3,
                'is_active': False  # Inactive for testing
            }
        ]
        
        created_count = 0
        for i in range(min(count, len(sample_posts))):
            post_data = sample_posts[i]
            
            # Check if post with this URL already exists
            if not InstagramPost.objects.filter(post_url=post_data['post_url']).exists():
                InstagramPost.objects.create(**post_data)
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created sample post: {post_data["post_url"]}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Post already exists: {post_data["post_url"]}')
                )
        
        if created_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'\nSuccessfully created {created_count} sample Instagram posts!')
            )
            self.stdout.write('You can now test the management interface at:')
            self.stdout.write('- Admin: /admin/main/instagrampost/')
            self.stdout.write('- Quick Add: /admin/instagram/quick-add/')
            self.stdout.write('- Preview: /admin/instagram/preview/<post_id>/')
        else:
            self.stdout.write(
                self.style.WARNING('No new posts were created (they may already exist)')
            )