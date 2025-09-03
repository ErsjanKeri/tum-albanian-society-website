"""
Caching utilities for Instagram embed data and other cached content
"""
import logging
from typing import Optional, Any, Dict
from django.core.cache import cache
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

logger = logging.getLogger(__name__)


class InstagramCacheManager:
    """Manager for Instagram embed data caching"""
    
    # Cache key prefixes
    EMBED_PREFIX = "instagram_embed"
    VALIDATION_PREFIX = "instagram_validation"
    POST_DATA_PREFIX = "instagram_post_data"
    
    # Cache timeouts (in seconds)
    EMBED_TIMEOUT = 60 * 60 * 24  # 24 hours for successful embeds
    EMBED_ERROR_TIMEOUT = 60 * 5  # 5 minutes for failed embeds
    VALIDATION_TIMEOUT = 60 * 30  # 30 minutes for URL validation
    POST_DATA_TIMEOUT = 60 * 60 * 2  # 2 hours for post metadata
    
    @classmethod
    def get_embed_cache_key(cls, post_url: str) -> str:
        """Generate cache key for embed data"""
        import hashlib
        url_hash = hashlib.md5(post_url.encode()).hexdigest()
        return f"{cls.EMBED_PREFIX}_{url_hash}"
    
    @classmethod
    def get_validation_cache_key(cls, post_url: str) -> str:
        """Generate cache key for URL validation"""
        import hashlib
        url_hash = hashlib.md5(post_url.encode()).hexdigest()
        return f"{cls.VALIDATION_PREFIX}_{url_hash}"
    
    @classmethod
    def get_post_data_cache_key(cls, post_id: int) -> str:
        """Generate cache key for post data"""
        return f"{cls.POST_DATA_PREFIX}_{post_id}"
    
    @classmethod
    def cache_embed_data(cls, post_url: str, embed_data: Dict, success: bool = True) -> None:
        """Cache Instagram embed data"""
        try:
            cache_key = cls.get_embed_cache_key(post_url)
            timeout = cls.EMBED_TIMEOUT if success else cls.EMBED_ERROR_TIMEOUT
            
            # Add cache metadata
            cached_data = {
                **embed_data,
                'cached_at': timezone.now().isoformat(),
                'cache_timeout': timeout
            }
            
            cache.set(cache_key, cached_data, timeout)
            logger.info(f"Cached Instagram embed data for {post_url} (success: {success})")
            
        except Exception as e:
            logger.error(f"Failed to cache Instagram embed data for {post_url}: {str(e)}")
    
    @classmethod
    def get_cached_embed_data(cls, post_url: str) -> Optional[Dict]:
        """Get cached Instagram embed data"""
        try:
            cache_key = cls.get_embed_cache_key(post_url)
            cached_data = cache.get(cache_key)
            
            if cached_data:
                logger.info(f"Retrieved cached Instagram embed data for {post_url}")
                return cached_data
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to retrieve cached Instagram embed data for {post_url}: {str(e)}")
            return None
    
    @classmethod
    def cache_validation_result(cls, post_url: str, is_valid: bool, error_message: str = "") -> None:
        """Cache URL validation result"""
        try:
            cache_key = cls.get_validation_cache_key(post_url)
            validation_data = {
                'is_valid': is_valid,
                'error_message': error_message,
                'validated_at': timezone.now().isoformat()
            }
            
            cache.set(cache_key, validation_data, cls.VALIDATION_TIMEOUT)
            logger.info(f"Cached validation result for {post_url} (valid: {is_valid})")
            
        except Exception as e:
            logger.error(f"Failed to cache validation result for {post_url}: {str(e)}")
    
    @classmethod
    def get_cached_validation_result(cls, post_url: str) -> Optional[Dict]:
        """Get cached URL validation result"""
        try:
            cache_key = cls.get_validation_cache_key(post_url)
            return cache.get(cache_key)
            
        except Exception as e:
            logger.error(f"Failed to retrieve cached validation result for {post_url}: {str(e)}")
            return None
    
    @classmethod
    def cache_post_data(cls, post_id: int, post_data: Dict) -> None:
        """Cache processed post data"""
        try:
            cache_key = cls.get_post_data_cache_key(post_id)
            cached_data = {
                **post_data,
                'cached_at': timezone.now().isoformat()
            }
            
            cache.set(cache_key, cached_data, cls.POST_DATA_TIMEOUT)
            logger.info(f"Cached post data for post ID {post_id}")
            
        except Exception as e:
            logger.error(f"Failed to cache post data for post ID {post_id}: {str(e)}")
    
    @classmethod
    def get_cached_post_data(cls, post_id: int) -> Optional[Dict]:
        """Get cached post data"""
        try:
            cache_key = cls.get_post_data_cache_key(post_id)
            return cache.get(cache_key)
            
        except Exception as e:
            logger.error(f"Failed to retrieve cached post data for post ID {post_id}: {str(e)}")
            return None
    
    @classmethod
    def clear_post_cache(cls, post_url: str = None, post_id: int = None) -> None:
        """Clear cache for specific post"""
        try:
            if post_url:
                # Clear embed and validation cache
                embed_key = cls.get_embed_cache_key(post_url)
                validation_key = cls.get_validation_cache_key(post_url)
                cache.delete_many([embed_key, validation_key])
                logger.info(f"Cleared cache for post URL: {post_url}")
            
            if post_id:
                # Clear post data cache
                post_data_key = cls.get_post_data_cache_key(post_id)
                cache.delete(post_data_key)
                logger.info(f"Cleared cache for post ID: {post_id}")
                
        except Exception as e:
            logger.error(f"Failed to clear cache: {str(e)}")
    
    @classmethod
    def clear_all_instagram_cache(cls) -> None:
        """Clear all Instagram-related cache (use with caution)"""
        try:
            # This is a simplified approach - in production you might want to use cache versioning
            logger.warning("Clearing all Instagram cache - this operation is not implemented for safety")
            # In a real implementation, you would need to track cache keys or use cache tags
            
        except Exception as e:
            logger.error(f"Failed to clear all Instagram cache: {str(e)}")
    
    @classmethod
    def get_cache_stats(cls) -> Dict:
        """Get cache statistics (if supported by cache backend)"""
        try:
            # This depends on the cache backend - Redis supports this, dummy cache doesn't
            if hasattr(cache, '_cache') and hasattr(cache._cache, 'info'):
                return cache._cache.info()
            else:
                return {'message': 'Cache statistics not available for this backend'}
                
        except Exception as e:
            logger.error(f"Failed to get cache statistics: {str(e)}")
            return {'error': str(e)}


class CacheWarmer:
    """Utility for warming up Instagram embed cache"""
    
    @classmethod
    def warm_instagram_cache(cls, post_urls: list) -> Dict:
        """Warm up cache for multiple Instagram posts"""
        from main.services.instagram_service import instagram_service
        
        results = {
            'success': 0,
            'failed': 0,
            'errors': []
        }
        
        for post_url in post_urls:
            try:
                embed_data = instagram_service.get_embed_data(post_url, use_cache=False)
                if embed_data['success']:
                    results['success'] += 1
                else:
                    results['failed'] += 1
                    results['errors'].append(f"{post_url}: {embed_data.get('error', 'Unknown error')}")
                    
            except Exception as e:
                results['failed'] += 1
                results['errors'].append(f"{post_url}: {str(e)}")
        
        logger.info(f"Cache warming completed: {results['success']} success, {results['failed']} failed")
        return results
    
    @classmethod
    def warm_active_posts_cache(cls) -> Dict:
        """Warm up cache for all active Instagram posts"""
        from main.models import InstagramPost
        
        active_posts = InstagramPost.objects.filter(is_active=True).values_list('post_url', flat=True)
        return cls.warm_instagram_cache(list(active_posts))