"""
Instagram oEmbed integration service for reliable post display
"""
import re
import json
import requests
import logging
from typing import Dict, Optional, Tuple
from urllib.parse import quote
from django.core.cache import cache
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


logger = logging.getLogger(__name__)


class InstagramEmbedService:
    """Service for handling Instagram oEmbed integration"""
    
    OEMBED_URL = "https://graph.facebook.com/v18.0/instagram_oembed"
    CACHE_TIMEOUT = 60 * 60 * 24  # 24 hours
    REQUEST_TIMEOUT = 10  # 10 seconds
    
    def __init__(self):
        self.access_token = getattr(settings, 'INSTAGRAM_ACCESS_TOKEN', None)
    
    def get_embed_data(self, post_url: str, use_cache: bool = True) -> Dict:
        """
        Get Instagram embed data using oEmbed API
        
        Args:
            post_url: Instagram post URL
            use_cache: Whether to use cached data
            
        Returns:
            Dict containing embed data or error information
        """
        # Try to get from cache first
        if use_cache:
            try:
                from main.utils.cache_utils import InstagramCacheManager
                cached_data = InstagramCacheManager.get_cached_embed_data(post_url)
                if cached_data:
                    return cached_data
            except ImportError:
                # Fallback to direct cache access
                cache_key = f"instagram_embed_{self._generate_cache_key(post_url)}"
                cached_data = cache.get(cache_key)
                if cached_data:
                    logger.info(f"Retrieved Instagram embed data from cache for {post_url}")
                    return cached_data
        
        # Validate Instagram URL
        if not self.is_valid_instagram_url(post_url):
            error_data = {
                'success': False,
                'error': 'Invalid Instagram URL format',
                'fallback_data': self._get_fallback_data(post_url)
            }
            return error_data
        
        try:
            # Make oEmbed API request
            embed_data = self._fetch_oembed_data(post_url)
            
            # Cache the response using cache manager
            try:
                from main.utils.cache_utils import InstagramCacheManager
                InstagramCacheManager.cache_embed_data(post_url, embed_data, embed_data['success'])
            except ImportError:
                # Fallback to direct cache access
                cache_key = f"instagram_embed_{self._generate_cache_key(post_url)}"
                timeout = self.CACHE_TIMEOUT if embed_data['success'] else 60 * 5
                cache.set(cache_key, embed_data, timeout)
            
            if embed_data['success']:
                logger.info(f"Successfully fetched and cached Instagram embed data for {post_url}")
            else:
                logger.warning(f"Failed to fetch Instagram embed data for {post_url}: {embed_data.get('error')}")
            
            return embed_data
            
        except Exception as e:
            logger.error(f"Exception while fetching Instagram embed data for {post_url}: {str(e)}")
            error_data = {
                'success': False,
                'error': f'Service error: {str(e)}',
                'fallback_data': self._get_fallback_data(post_url)
            }
            # Cache error for short time
            try:
                from main.utils.cache_utils import InstagramCacheManager
                InstagramCacheManager.cache_embed_data(post_url, error_data, False)
            except ImportError:
                cache_key = f"instagram_embed_{self._generate_cache_key(post_url)}"
                cache.set(cache_key, error_data, 60 * 5)  # 5 minutes
            return error_data
    
    def _fetch_oembed_data(self, post_url: str) -> Dict:
        """Fetch data from Instagram oEmbed API"""
        try:
            # Check if we have access token - if not, skip API call and use fallback
            if not self.access_token:
                logger.info(f"No Instagram access token configured, using fallback for {post_url}")
                return {
                    'success': False,
                    'error': 'Instagram API access not configured - using fallback display',
                    'fallback_data': self._get_fallback_data(post_url),
                    'use_fallback': True
                }
            
            # Prepare request parameters
            params = {
                'url': post_url,
                'omitscript': 'true',  # Don't include Instagram's embed script
                'hidecaption': 'false',  # Include caption
                'maxwidth': 540,  # Max width for responsive design
                'access_token': self.access_token
            }
            
            # Make API request
            response = requests.get(
                self.OEMBED_URL,
                params=params,
                timeout=self.REQUEST_TIMEOUT,
                headers={
                    'User-Agent': 'Mozilla/5.0 (compatible; InstagramEmbedBot/1.0)',
                    'Accept': 'application/json'
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract useful information
                embed_data = {
                    'success': True,
                    'html': data.get('html', ''),
                    'width': data.get('width'),
                    'height': data.get('height'),
                    'thumbnail_url': data.get('thumbnail_url', ''),
                    'author_name': data.get('author_name', ''),
                    'author_url': data.get('author_url', ''),
                    'provider_name': data.get('provider_name', 'Instagram'),
                    'provider_url': data.get('provider_url', 'https://www.instagram.com'),
                    'title': data.get('title', ''),
                    'cached_at': timezone.now().isoformat(),
                    'original_url': post_url,
                    # Additional media information
                    'media_type': self._detect_media_type(data.get('html', '')),
                    'is_carousel': self._detect_carousel(data.get('html', ''))
                }
                
                return embed_data
            elif response.status_code == 403:
                # Handle authentication errors specifically
                error_data = response.json() if response.content else {}
                error_message = error_data.get('error', {}).get('message', 'Authentication failed')
                
                logger.warning(f"Instagram API authentication failed for {post_url}: {error_message}")
                return {
                    'success': False,
                    'error': f'Instagram API authentication required: {error_message}',
                    'fallback_data': self._get_fallback_data(post_url),
                    'use_fallback': True,
                    'auth_error': True
                }
            else:
                error_text = response.text
                try:
                    error_data = response.json()
                    error_message = error_data.get('error', {}).get('message', error_text)
                except:
                    error_message = error_text
                
                return {
                    'success': False,
                    'error': f'API returned status {response.status_code}: {error_message}',
                    'fallback_data': self._get_fallback_data(post_url),
                    'use_fallback': True
                }
                
        except requests.RequestException as e:
            return {
                'success': False,
                'error': f'Request failed: {str(e)}',
                'fallback_data': self._get_fallback_data(post_url),
                'use_fallback': True
            }
        except json.JSONDecodeError as e:
            return {
                'success': False,
                'error': f'Invalid JSON response: {str(e)}',
                'fallback_data': self._get_fallback_data(post_url),
                'use_fallback': True
            }
    
    def _detect_media_type(self, html: str) -> str:
        """Detect media type from embed HTML"""
        if not html:
            return 'unknown'
        
        html_lower = html.lower()
        if 'video' in html_lower:
            return 'video'
        elif 'carousel' in html_lower or 'multiple' in html_lower:
            return 'carousel'
        else:
            return 'image'
    
    def _detect_carousel(self, html: str) -> bool:
        """Detect if post is a carousel from embed HTML"""
        if not html:
            return False
        
        # Look for carousel indicators in the HTML
        carousel_indicators = ['carousel', 'multiple', 'slide', 'swipe']
        html_lower = html.lower()
        return any(indicator in html_lower for indicator in carousel_indicators)
    
    def _get_fallback_data(self, post_url: str, media_urls: list = None) -> Dict:
        """Generate fallback data when oEmbed fails"""
        # Determine if it's a carousel based on URL or media count
        is_carousel = self._is_carousel_url(post_url) or (media_urls and len(media_urls) > 1)
        icon = "🎠" if is_carousel else "📷"
        text = "Instagram Carousel" if is_carousel else "Instagram Post"
        
        return {
            'html': f'''
                <div class="instagram-fallback">
                    <div class="instagram-fallback-content">
                        <div class="instagram-fallback-icon">{icon}</div>
                        <p class="instagram-fallback-text">{text}</p>
                        <a href="{post_url}" target="_blank" rel="noopener noreferrer" class="instagram-fallback-link">
                            View on Instagram
                        </a>
                    </div>
                </div>
            ''',
            'width': 540,
            'height': 300,
            'thumbnail_url': media_urls[0] if media_urls else '',
            'author_name': 'Instagram User',
            'is_fallback': True,
            'is_carousel': is_carousel,
            'media_count': len(media_urls) if media_urls else 1,
            'original_url': post_url
        }
    
    def _is_carousel_url(self, post_url: str) -> bool:
        """Check if URL indicates a carousel post"""
        # Instagram carousel posts sometimes have specific URL patterns
        # This is a basic heuristic - in practice, you'd need to check the actual post
        return False  # We'll rely on the embed data or manual specification
    
    def is_valid_instagram_url(self, url: str) -> bool:
        """Validate Instagram URL format"""
        if not url or not isinstance(url, str):
            return False
        
        instagram_patterns = [
            r'https?://(?:www\.)?instagram\.com/p/[A-Za-z0-9_-]+/?(?:\?.*)?$',
            r'https?://(?:www\.)?instagram\.com/reel/[A-Za-z0-9_-]+/?(?:\?.*)?$',
            r'https?://(?:www\.)?instagram\.com/tv/[A-Za-z0-9_-]+/?(?:\?.*)?$'
        ]
        
        return any(re.match(pattern, url) for pattern in instagram_patterns)
    
    def validate_post_content(self, post_url: str, media_url: str = None) -> Tuple[bool, str]:
        """
        Validate Instagram post content
        
        Args:
            post_url: Instagram post URL
            media_url: Optional direct media URL
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Validate post URL format
        if not self.is_valid_instagram_url(post_url):
            return False, "Invalid Instagram URL format. Please use a valid Instagram post, reel, or IGTV URL."
        
        # Validate media URL if provided
        if media_url:
            if not self._is_valid_media_url(media_url):
                return False, "Invalid media URL format. Please provide a direct link to an image or video."
        
        # Try to fetch embed data to verify post exists
        try:
            embed_data = self.get_embed_data(post_url, use_cache=False)
            if not embed_data['success']:
                return False, f"Could not access Instagram post: {embed_data.get('error', 'Unknown error')}"
        except Exception as e:
            logger.warning(f"Could not validate Instagram post {post_url}: {str(e)}")
            # Don't fail validation if we can't check - the post might still be valid
            pass
        
        return True, ""
    
    def _is_valid_media_url(self, url: str) -> bool:
        """Check if URL appears to be a valid media URL"""
        if not url or not isinstance(url, str):
            return False
        
        try:
            # Check if it's a valid URL format
            if not url.startswith(('http://', 'https://')):
                return False
            
            # Check for common media file extensions or Instagram CDN patterns
            media_patterns = [
                r'.*\.(jpg|jpeg|png|gif|webp|mp4|mov)(\?.*)?$',  # File extensions
                r'.*instagram\.com.*',  # Instagram CDN
                r'.*fbcdn\.net.*',  # Facebook CDN (used by Instagram)
                r'.*cdninstagram\.com.*'  # Instagram CDN
            ]
            
            return any(re.match(pattern, url, re.IGNORECASE) for pattern in media_patterns)
            
        except Exception:
            return False
    
    def _generate_cache_key(self, post_url: str) -> str:
        """Generate a cache key from post URL"""
        import hashlib
        return hashlib.md5(post_url.encode()).hexdigest()
    
    def clear_cache(self, post_url: str = None):
        """Clear cached embed data"""
        if post_url:
            cache_key = f"instagram_embed_{self._generate_cache_key(post_url)}"
            cache.delete(cache_key)
            logger.info(f"Cleared cache for Instagram post: {post_url}")
        else:
            # Clear all Instagram embed cache (this is a simplified approach)
            # In production, you might want to use cache versioning or tags
            logger.info("Cache clearing for all Instagram embeds not implemented")
    
    def get_embed_html_safe(self, post_url: str) -> str:
        """
        Get safe HTML for Instagram embed with fallback
        
        Args:
            post_url: Instagram post URL
            
        Returns:
            Safe HTML string for embedding
        """
        embed_data = self.get_embed_data(post_url)
        
        if embed_data['success'] and embed_data.get('html'):
            return embed_data['html']
        else:
            # Return fallback HTML
            fallback_data = embed_data.get('fallback_data', self._get_fallback_data(post_url))
            return fallback_data['html']


# Global service instance
instagram_service = InstagramEmbedService()