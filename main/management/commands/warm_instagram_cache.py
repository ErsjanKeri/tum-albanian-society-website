"""
Management command to warm up Instagram embed cache
"""
from django.core.management.base import BaseCommand
from main.utils.cache_utils import CacheWarmer, InstagramCacheManager
from main.models import InstagramPost


class Command(BaseCommand):
    help = 'Warm up Instagram embed cache for better performance'

    def add_arguments(self, parser):
        parser.add_argument(
            '--active-only',
            action='store_true',
            help='Only warm cache for active posts'
        )
        parser.add_argument(
            '--clear-first',
            action='store_true',
            help='Clear existing cache before warming'
        )
        parser.add_argument(
            '--post-ids',
            nargs='+',
            type=int,
            help='Specific post IDs to warm cache for'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Instagram cache warming...'))
        
        # Clear cache if requested
        if options['clear_first']:
            self.stdout.write('Clearing existing cache...')
            # Note: This is a simplified approach - in production you might want more granular control
            self.stdout.write(self.style.WARNING('Cache clearing not fully implemented for safety'))
        
        # Determine which posts to warm cache for
        if options['post_ids']:
            # Specific post IDs
            posts = InstagramPost.objects.filter(id__in=options['post_ids'])
            post_urls = list(posts.values_list('post_url', flat=True))
            self.stdout.write(f'Warming cache for {len(post_urls)} specific posts...')
        elif options['active_only']:
            # Only active posts
            results = CacheWarmer.warm_active_posts_cache()
            self.display_results(results)
            return
        else:
            # All posts
            posts = InstagramPost.objects.all()
            post_urls = list(posts.values_list('post_url', flat=True))
            self.stdout.write(f'Warming cache for all {len(post_urls)} posts...')
        
        # Warm the cache
        if post_urls:
            results = CacheWarmer.warm_instagram_cache(post_urls)
            self.display_results(results)
        else:
            self.stdout.write(self.style.WARNING('No posts found to warm cache for'))

    def display_results(self, results):
        """Display cache warming results"""
        self.stdout.write(
            self.style.SUCCESS(
                f'Cache warming completed:\n'
                f'  Success: {results["success"]}\n'
                f'  Failed: {results["failed"]}'
            )
        )
        
        if results['errors']:
            self.stdout.write(self.style.ERROR('Errors encountered:'))
            for error in results['errors']:
                self.stdout.write(f'  - {error}')
        
        # Display cache statistics if available
        try:
            stats = InstagramCacheManager.get_cache_stats()
            if 'error' not in stats and 'message' not in stats:
                self.stdout.write(self.style.SUCCESS('Cache statistics:'))
                for key, value in stats.items():
                    self.stdout.write(f'  {key}: {value}')
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Could not retrieve cache stats: {e}'))