"""
Management command to test Instagram service functionality
"""
from django.core.management.base import BaseCommand
from main.services.instagram_service import instagram_service
from main.models import InstagramPost


class Command(BaseCommand):
    help = 'Test Instagram service functionality'

    def add_arguments(self, parser):
        parser.add_argument(
            '--url',
            type=str,
            help='Instagram post URL to test'
        )
        parser.add_argument(
            '--validate-only',
            action='store_true',
            help='Only validate URL format, don\'t fetch embed data'
        )
        parser.add_argument(
            '--test-all-posts',
            action='store_true',
            help='Test all Instagram posts in the database'
        )

    def handle(self, *args, **options):
        if options['test_all_posts']:
            self.test_all_posts()
        elif options['url']:
            self.test_single_url(options['url'], options['validate_only'])
        else:
            self.stdout.write(
                self.style.ERROR('Please provide --url or use --test-all-posts')
            )

    def test_single_url(self, url, validate_only=False):
        """Test a single Instagram URL"""
        self.stdout.write(f'Testing Instagram URL: {url}')
        self.stdout.write('-' * 60)
        
        # Test URL validation
        is_valid = instagram_service.is_valid_instagram_url(url)
        self.stdout.write(f'URL Format Valid: {is_valid}')
        
        if not is_valid:
            self.stdout.write(self.style.ERROR('Invalid URL format'))
            return
        
        if validate_only:
            self.stdout.write(self.style.SUCCESS('URL validation passed'))
            return
        
        # Test content validation
        try:
            is_valid, error_message = instagram_service.validate_post_content(url)
            self.stdout.write(f'Content Valid: {is_valid}')
            if not is_valid:
                self.stdout.write(f'Error: {error_message}')
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Content validation failed: {str(e)}'))
        
        # Test embed data fetching
        try:
            self.stdout.write('Fetching embed data...')
            embed_data = instagram_service.get_embed_data(url, use_cache=False)
            
            self.stdout.write(f'Embed Success: {embed_data["success"]}')
            
            if embed_data['success']:
                self.stdout.write(self.style.SUCCESS('Embed data retrieved successfully'))
                self.stdout.write(f'Width: {embed_data.get("width", "N/A")}')
                self.stdout.write(f'Height: {embed_data.get("height", "N/A")}')
                self.stdout.write(f'Author: {embed_data.get("author_name", "N/A")}')
                self.stdout.write(f'Thumbnail: {embed_data.get("thumbnail_url", "N/A")}')
                
                if embed_data.get('html'):
                    html_preview = embed_data['html'][:100] + "..." if len(embed_data['html']) > 100 else embed_data['html']
                    self.stdout.write(f'HTML Preview: {html_preview}')
            else:
                self.stdout.write(self.style.ERROR(f'Embed failed: {embed_data.get("error", "Unknown error")}'))
                
                # Show fallback data
                fallback_data = embed_data.get('fallback_data')
                if fallback_data:
                    self.stdout.write('Fallback data available')
                    
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Embed data fetch failed: {str(e)}'))

    def test_all_posts(self):
        """Test all Instagram posts in the database"""
        posts = InstagramPost.objects.all()
        
        if not posts.exists():
            self.stdout.write(self.style.WARNING('No Instagram posts found in database'))
            return
        
        self.stdout.write(f'Testing {posts.count()} Instagram posts...')
        self.stdout.write('=' * 60)
        
        success_count = 0
        failed_count = 0
        
        for post in posts:
            self.stdout.write(f'\nTesting Post ID {post.id}:')
            self.stdout.write(f'URL: {post.post_url}')
            self.stdout.write(f'Active: {post.is_active}')
            
            try:
                embed_data = instagram_service.get_embed_data(post.post_url, use_cache=False)
                
                if embed_data['success']:
                    self.stdout.write(self.style.SUCCESS('✓ Success'))
                    success_count += 1
                else:
                    self.stdout.write(self.style.ERROR(f'✗ Failed: {embed_data.get("error", "Unknown error")}'))
                    failed_count += 1
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Exception: {str(e)}'))
                failed_count += 1
        
        # Summary
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(f'Test Summary:')
        self.stdout.write(f'  Total Posts: {posts.count()}')
        self.stdout.write(f'  Successful: {success_count}')
        self.stdout.write(f'  Failed: {failed_count}')
        
        if success_count == posts.count():
            self.stdout.write(self.style.SUCCESS('All tests passed!'))
        elif success_count > 0:
            self.stdout.write(self.style.WARNING('Some tests failed'))
        else:
            self.stdout.write(self.style.ERROR('All tests failed'))