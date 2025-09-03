"""
Template tags for Instagram embed display
"""
from django import template
from django.utils.safestring import mark_safe
from django.utils.html import escape
from main.services.instagram_service import instagram_service
from main.models import InstagramPost, InstagramConfig
import logging

logger = logging.getLogger(__name__)
register = template.Library()


@register.simple_tag
def instagram_embed(post_url, css_class="instagram-embed"):
    """
    Template tag to embed Instagram post with fallback
    
    Usage: {% instagram_embed post.post_url %}
    """
    try:
        embed_html = instagram_service.get_embed_html_safe(post_url)
        
        # Wrap in container div with custom CSS class
        wrapped_html = f'<div class="{css_class}">{embed_html}</div>'
        
        return mark_safe(wrapped_html)
    except Exception as e:
        logger.error(f"Error in instagram_embed template tag: {str(e)}")
        # Return safe fallback
        fallback_html = f'''
            <div class="{css_class} instagram-error">
                <div class="instagram-fallback-content">
                    <div class="instagram-fallback-icon">⚠️</div>
                    <p class="instagram-fallback-text">Unable to load Instagram post</p>
                    <a href="{escape(post_url)}" target="_blank" rel="noopener noreferrer" class="instagram-fallback-link">
                        View on Instagram
                    </a>
                </div>
            </div>
        '''
        return mark_safe(fallback_html)


@register.simple_tag
def instagram_embed_data(post_url):
    """
    Get Instagram embed data as context variable
    
    Usage: {% instagram_embed_data post.post_url as embed_data %}
    """
    try:
        return instagram_service.get_embed_data(post_url)
    except Exception as e:
        logger.error(f"Error in instagram_embed_data template tag: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'fallback_data': instagram_service._get_fallback_data(post_url)
        }


@register.inclusion_tag('main/components/instagram_post.html')
def render_instagram_post(post, show_caption=True, css_class="instagram-post"):
    """
    Render Instagram post with custom template
    
    Usage: {% render_instagram_post post %}
    """
    try:
        # Get configuration
        config = InstagramConfig.objects.first()
        max_length = config.max_caption_length if config and config.max_caption_length > 0 else 150
        
        # Process caption with hashtag/mention highlighting
        caption = post.caption
        full_caption = process_instagram_caption(caption) if caption else ""
        
        # Create truncated version for "Read More" functionality
        truncated_caption = None
        needs_read_more = False
        
        if caption and len(caption) > max_length:
            needs_read_more = True
            truncated_text = caption[:max_length].rsplit(' ', 1)[0]
            truncated_caption = process_instagram_caption(truncated_text)
        
        # FIXED: Only try API if we don't have manual media URLs
        embed_data = {'success': False, 'use_fallback': True}
        
        if not post.get_all_media_urls():
            # Only call API if no manual media URLs are provided
            embed_data = instagram_service.get_embed_data(post.post_url)
        
        return {
            'post': post,
            'embed_data': embed_data,
            'caption': caption,
            'full_caption': full_caption,
            'truncated_caption': truncated_caption,
            'needs_read_more': needs_read_more,
            'max_caption_length': max_length,
            'show_caption': show_caption and (config.show_captions if config else True),
            'css_class': css_class,
            'is_fallback': True,  # Always use fallback for manual posts
            'config': config
        }
    except Exception as e:
        logger.error(f"Error in render_instagram_post template tag: {str(e)}")
        return {
            'post': post,
            'embed_data': {'success': False, 'error': str(e)},
            'caption': post.caption,
            'full_caption': post.caption,
            'truncated_caption': None,
            'needs_read_more': False,
            'show_caption': show_caption,
            'css_class': css_class,
            'is_fallback': True,
            'config': None
        }


@register.simple_tag
def get_active_instagram_posts(limit=None):
    """
    Get active Instagram posts for display
    
    Usage: {% get_active_instagram_posts as posts %}
    """
    try:
        posts = InstagramPost.objects.filter(is_active=True)
        
        if limit:
            posts = posts[:limit]
        else:
            # Use config limit if available
            config = InstagramConfig.objects.first()
            if config:
                posts = posts[:config.posts_per_page]
        
        return posts
    except Exception as e:
        logger.error(f"Error in get_active_instagram_posts template tag: {str(e)}")
        return InstagramPost.objects.none()


@register.simple_tag
def get_instagram_config():
    """
    Get Instagram configuration
    
    Usage: {% get_instagram_config as config %}
    """
    try:
        return InstagramConfig.objects.first()
    except Exception as e:
        logger.error(f"Error in get_instagram_config template tag: {str(e)}")
        return None


@register.filter
def truncate_caption(caption, max_length=150):
    """
    Truncate Instagram caption to specified length
    
    Usage: {{ post.caption|truncate_caption:100 }}
    """
    if not caption or not max_length:
        return caption
    
    if len(caption) <= max_length:
        return caption
    
    return caption[:max_length].rsplit(' ', 1)[0] + "..."


@register.filter
def highlight_hashtags(caption):
    """
    Highlight hashtags in Instagram caption
    
    Usage: {{ post.caption|highlight_hashtags }}
    """
    if not caption:
        return caption
    
    import re
    from django.utils.safestring import mark_safe
    from django.utils.html import escape
    
    # Escape the caption first for safety
    escaped_caption = escape(caption)
    
    # Pattern to match hashtags (# followed by alphanumeric characters and underscores)
    hashtag_pattern = r'#([A-Za-z0-9_]+)'
    
    def replace_hashtag(match):
        hashtag = match.group(1)
        full_hashtag = match.group(0)
        # Create a link to Instagram hashtag search
        instagram_hashtag_url = f"https://www.instagram.com/explore/tags/{hashtag}/"
        return f'<a href="{instagram_hashtag_url}" target="_blank" rel="noopener noreferrer" class="instagram-hashtag">#{hashtag}</a>'
    
    # Replace hashtags with links
    highlighted_caption = re.sub(hashtag_pattern, replace_hashtag, escaped_caption)
    
    return mark_safe(highlighted_caption)


@register.filter
def highlight_mentions(caption):
    """
    Highlight @mentions in Instagram caption
    
    Usage: {{ post.caption|highlight_mentions }}
    """
    if not caption:
        return caption
    
    import re
    from django.utils.safestring import mark_safe
    from django.utils.html import escape
    
    # Escape the caption first for safety
    escaped_caption = escape(caption)
    
    # Pattern to match mentions (@ followed by alphanumeric characters, dots, and underscores)
    mention_pattern = r'@([A-Za-z0-9_.]+)'
    
    def replace_mention(match):
        username = match.group(1)
        full_mention = match.group(0)
        # Create a link to Instagram profile
        instagram_profile_url = f"https://www.instagram.com/{username}/"
        return f'<a href="{instagram_profile_url}" target="_blank" rel="noopener noreferrer" class="instagram-mention">@{username}</a>'
    
    # Replace mentions with links
    highlighted_caption = re.sub(mention_pattern, replace_mention, escaped_caption)
    
    return mark_safe(highlighted_caption)


@register.filter
def process_instagram_caption(caption, max_length=None):
    """
    Process Instagram caption with hashtag/mention highlighting and optional truncation
    
    Usage: {{ post.caption|process_instagram_caption:150 }}
    """
    if not caption:
        return caption
    
    # First highlight hashtags and mentions
    processed_caption = highlight_mentions(highlight_hashtags(caption))
    
    # Then truncate if needed
    if max_length and len(caption) > max_length:
        # We need to be careful with truncation since we now have HTML
        # For now, we'll truncate the original text and then process it
        truncated_text = truncate_caption(caption, max_length)
        processed_caption = highlight_mentions(highlight_hashtags(truncated_text))
    
    return processed_caption


@register.simple_tag
def instagram_fallback_html(post_url, css_class="instagram-fallback"):
    """
    Generate fallback HTML for Instagram post
    
    Usage: {% instagram_fallback_html post.post_url %}
    """
    fallback_html = f'''
        <div class="{css_class}">
            <div class="instagram-fallback-content">
                <div class="instagram-fallback-icon">📷</div>
                <p class="instagram-fallback-text">Instagram Post</p>
                <a href="{escape(post_url)}" target="_blank" rel="noopener noreferrer" class="instagram-fallback-link">
                    View on Instagram
                </a>
            </div>
        </div>
    '''
    return mark_safe(fallback_html)


@register.simple_tag
def validate_instagram_url(url):
    """
    Validate Instagram URL format
    
    Usage: {% validate_instagram_url post.post_url as is_valid %}
    """
    try:
        return instagram_service.is_valid_instagram_url(url)
    except Exception:
        return False


@register.simple_tag
def check_instagram_post_availability(post):
    """
    Check if Instagram post is still available
    
    Usage: {% check_instagram_post_availability post as is_available %}
    """
    try:
        embed_data = instagram_service.get_embed_data(post.post_url, use_cache=True)
        
        # Check for specific error messages that indicate deleted/unavailable posts
        if not embed_data['success']:
            error_msg = embed_data.get('error', '').lower()
            unavailable_indicators = [
                'not found',
                'deleted',
                'removed',
                'unavailable',
                'private',
                'restricted',
                '404',
                'does not exist'
            ]
            
            is_unavailable = any(indicator in error_msg for indicator in unavailable_indicators)
            
            return {
                'is_available': False,
                'is_deleted': is_unavailable,
                'error': embed_data.get('error', 'Unknown error'),
                'can_retry': not is_unavailable  # Can retry if it's not definitely deleted
            }
        
        return {
            'is_available': True,
            'is_deleted': False,
            'error': None,
            'can_retry': False
        }
        
    except Exception as e:
        logger.error(f"Error checking Instagram post availability for {post.post_url}: {str(e)}")
        return {
            'is_available': False,
            'is_deleted': False,
            'error': str(e),
            'can_retry': True
        }


@register.inclusion_tag('main/components/instagram_post_unavailable.html')
def render_unavailable_instagram_post(post, reason="unavailable"):
    """
    Render template for unavailable Instagram post
    
    Usage: {% render_unavailable_instagram_post post reason="deleted" %}
    """
    return {
        'post': post,
        'reason': reason,
        'show_retry': reason not in ['deleted', 'private', 'removed']
    }