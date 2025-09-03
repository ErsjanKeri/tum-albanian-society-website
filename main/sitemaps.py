from django.contrib.sitemaps import Sitemap 
from django.urls import reverse
from django.conf import settings
from django.utils import translation

from .models import * 

class StaticViewsSitemap(Sitemap):
    """
    Enhanced sitemap that includes all pages with multilingual support.
    Covers homepage and contact page in all supported languages.
    """
    priority = 0.8
    changefreq = 'weekly'
    protocol = 'http' if settings.DEBUG else 'https'
    
    def items(self):
        """Return all static pages that should be included in sitemap"""
        pages = []
        # Get all supported languages from settings
        languages = [lang[0] for lang in settings.LANGUAGES]
        
        # Define all available pages
        page_names = ['index', 'contact']
        
        # Create entries for each page in each language
        for page in page_names:
            for lang in languages:
                pages.append({
                    'page': page,
                    'language': lang
                })
        
        return pages
    
    def location(self, item):
        """Generate URL for each page/language combination"""
        page = item['page']
        language = item['language']
        
        # Activate the language for URL generation
        with translation.override(language):
            if language == 'en':
                # English is the default language, no prefix needed
                return reverse(page)
            else:
                # For other languages, include language prefix
                return f'/{language}{reverse(page)}'
    
    def lastmod(self, item):
        """Return last modification date - can be enhanced later with actual content dates"""
        return None
    
    def priority(self, item):
        """Set priority based on page importance"""
        if item['page'] == 'index':
            return 1.0  # Homepage has highest priority
        elif item['page'] == 'contact':
            return 0.7  # Contact page has high priority
        return 0.5  # Default priority for other pages


class EventsSitemap(Sitemap):
    """
    Sitemap for dynamic events content.
    Includes active upcoming events in all languages.
    """
    changefreq = 'daily'
    priority = 0.6
    protocol = 'http' if settings.DEBUG else 'https'
    
    def items(self):
        """Return active events for sitemap inclusion"""
        events = []
        languages = [lang[0] for lang in settings.LANGUAGES]
        
        # Get all active events
        active_events = UpcomingEvents.objects.filter(active=True)
        
        # Create entries for each event in each language
        for event in active_events:
            for lang in languages:
                events.append({
                    'event': event,
                    'language': lang
                })
        
        return events
    
    def location(self, item):
        """Generate URL for event pages - currently points to homepage with anchor"""
        language = item['language']
        
        with translation.override(language):
            if language == 'en':
                return f"{reverse('index')}#events"
            else:
                return f"/{language}{reverse('index')}#events"
    
    def lastmod(self, item):
        """Return last modification date of the event"""
        # Since events don't have a modified date, we can return None
        # or add a modified field to the model later
        return None
