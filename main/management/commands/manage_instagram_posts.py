"""
Management command for Instagram post administration
"""
import re
import requests
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
from main.models import InstagramPost


class Command(BaseCommand):
    help = 'Manage Instagram posts - add, list, activate, deactivate posts'

    def add_arguments(self, parser):
        parser.add_argument(
            'action',
            choices=['add', 'list', 'activate', 'deactivate', 'delete'],
            help='Action to perform'
        )
        parser.add_argument(
            '--url',
            type=str,
            help='Instagram post URL (required for add action)'
        )
        parser.add_argument(
            '--caption',
            type=str,
            help='Post caption (optional for add action)'
        )
        parser.add_argument(
            '--media-urls',
            nargs='+',
            help='Direct media URLs (optional for add action, multiple URLs for carousel)'
        )
        parser.add_argument(
            '--post-type',
            choices=['image', 'carousel', 'video', 'reel'],
            default='image',
            help='Type of Instagram post'
        )
        parser.add_argument(
            '--order',
            type=int,
            default=0,
            help='Display order (optional for add action)'
        )
        parser.add_argument(
            '--id',
            type=int,
            help='Post ID (required for activate/deactivate/delete actions)'
        )

    def handle(self, *args, **options):
        action = options['action']
        
        if action == 'add':
            self.add_post(options)
        elif action == 'list':
            self.list_posts()
        elif action == 'activate':
            self.activate_post(options['id'])
        elif action == 'deactivate':
            self.deactivate_post(options['id'])
        elif action == 'delete':
            self.delete_post(options['id'])

    def add_post(self, options):
        """Add a new Instagram post"""
        post_url = options.get('url')
        if not post_url:
            raise CommandError('--url is required for add action')
        
        # Validate Instagram URL format
        if not self.is_valid_instagram_url(post_url):
            raise CommandError('Invalid Instagram URL format')
        
        caption = options.get('caption', '')
        media_url = options.get('media_url', '')
        display_order = options.get('order', 0)
        
        # If media URL is not provided, try to extract from Instagram URL
        if not media_url:
            media_url = self.extract_media_url_from_post(post_url)
        
        try:
            post = InstagramPost.objects.create(
                caption=caption,
                media_url=media_url,
                post_url=post_url,
                display_order=display_order,
                is_active=True
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully added Instagram post with ID: {post.id}')
            )
        except ValidationError as e:
            raise CommandError(f'Validation error: {e}')
        except Exception as e:
            raise CommandError(f'Error creating post: {e}')

    def list_posts(self):
        """List all Instagram posts"""
        posts = InstagramPost.objects.all().order_by('display_order', '-created_at')
        
        if not posts.exists():
            self.stdout.write(self.style.WARNING('No Instagram posts found'))
            return
        
        self.stdout.write(self.style.SUCCESS('Instagram Posts:'))
        self.stdout.write('-' * 80)
        
        for post in posts:
            status = "ACTIVE" if post.is_active else "INACTIVE"
            caption_preview = (post.caption[:50] + "...") if len(post.caption) > 50 else post.caption
            
            self.stdout.write(
                f'ID: {post.id} | Order: {post.display_order} | Status: {status}\n'
                f'Caption: {caption_preview or "No caption"}\n'
                f'Post URL: {post.post_url}\n'
                f'Media URL: {post.media_url}\n'
                f'Created: {post.created_at.strftime("%Y-%m-%d %H:%M")}\n'
                + '-' * 80
            )

    def activate_post(self, post_id):
        """Activate an Instagram post"""
        if not post_id:
            raise CommandError('--id is required for activate action')
        
        try:
            post = InstagramPost.objects.get(id=post_id)
            post.is_active = True
            post.save()
            self.stdout.write(
                self.style.SUCCESS(f'Successfully activated post ID: {post_id}')
            )
        except InstagramPost.DoesNotExist:
            raise CommandError(f'Post with ID {post_id} not found')

    def deactivate_post(self, post_id):
        """Deactivate an Instagram post"""
        if not post_id:
            raise CommandError('--id is required for deactivate action')
        
        try:
            post = InstagramPost.objects.get(id=post_id)
            post.is_active = False
            post.save()
            self.stdout.write(
                self.style.SUCCESS(f'Successfully deactivated post ID: {post_id}')
            )
        except InstagramPost.DoesNotExist:
            raise CommandError(f'Post with ID {post_id} not found')

    def delete_post(self, post_id):
        """Delete an Instagram post"""
        if not post_id:
            raise CommandError('--id is required for delete action')
        
        try:
            post = InstagramPost.objects.get(id=post_id)
            post.delete()
            self.stdout.write(
                self.style.SUCCESS(f'Successfully deleted post ID: {post_id}')
            )
        except InstagramPost.DoesNotExist:
            raise CommandError(f'Post with ID {post_id} not found')

    def is_valid_instagram_url(self, url):
        """Validate Instagram URL format"""
        instagram_patterns = [
            r'https?://(?:www\.)?instagram\.com/p/[A-Za-z0-9_-]+/?',
            r'https?://(?:www\.)?instagram\.com/reel/[A-Za-z0-9_-]+/?',
            r'https?://(?:www\.)?instagram\.com/tv/[A-Za-z0-9_-]+/?'
        ]
        
        return any(re.match(pattern, url) for pattern in instagram_patterns)

    def extract_media_url_from_post(self, post_url):
        """
        Try to extract media URL from Instagram post URL
        This is a basic implementation - in production you might want to use Instagram's API
        """
        # For now, return empty string - admin will need to provide media URL manually
        # In a full implementation, you could use Instagram's oEmbed API or Basic Display API
        return ""