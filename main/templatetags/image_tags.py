from django import template
from django.utils.safestring import mark_safe
from django.templatetags.static import static
from urllib.parse import urlparse
import logging

# Try to import requests, but handle gracefully if not available
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

register = template.Library()
logger = logging.getLogger(__name__)


@register.simple_tag
def safe_image(image_url, alt_text="", css_class="", fallback_image="assets/img/placeholder.jpg", loading="lazy"):
    """
    Display an image with fallback support for broken or unavailable links.
    
    Args:
        image_url: The URL of the image to display
        alt_text: Alt text for accessibility
        css_class: CSS classes to apply to the image
        fallback_image: Path to fallback image (relative to static files)
        loading: Loading attribute (lazy, eager, auto)
    
    Returns:
        HTML img tag with fallback handling
    """
    if not image_url:
        # If no image URL provided, use fallback
        final_url = static(fallback_image)
        return mark_safe(f'<img src="{final_url}" alt="{alt_text}" class="{css_class}" loading="{loading}" />')
    
    # Check if the image URL is accessible
    if is_image_accessible(image_url):
        final_url = image_url
    else:
        # Use fallback image
        final_url = static(fallback_image)
        logger.warning(f"Image not accessible, using fallback: {image_url}")
    
    return mark_safe(f'<img src="{final_url}" alt="{alt_text}" class="{css_class}" loading="{loading}" onerror="this.src=\'{static(fallback_image)}\'; this.onerror=null;" />')


@register.simple_tag
def safe_image_with_placeholder(image_url, alt_text="", css_class="", width="400", height="300", loading="lazy"):
    """
    Display an image with a generated placeholder fallback.
    
    Args:
        image_url: The URL of the image to display
        alt_text: Alt text for accessibility
        css_class: CSS classes to apply to the image
        width: Width for placeholder
        height: Height for placeholder
        loading: Loading attribute (lazy, eager, auto)
    
    Returns:
        HTML img tag with placeholder fallback
    """
    if not image_url:
        # Generate placeholder URL
        placeholder_url = f"https://via.placeholder.com/{width}x{height}/cccccc/666666?text=No+Image"
        return mark_safe(f'<img src="{placeholder_url}" alt="{alt_text}" class="{css_class}" loading="{loading}" />')
    
    # Use the image with JavaScript fallback to placeholder
    placeholder_url = f"https://via.placeholder.com/{width}x{height}/cccccc/666666?text=Image+Not+Found"
    
    return mark_safe(f'<img src="{image_url}" alt="{alt_text}" class="{css_class}" loading="{loading}" onerror="this.src=\'{placeholder_url}\'; this.onerror=null;" />')


def is_image_accessible(url):
    """
    Check if an image URL is accessible.
    
    Args:
        url: The URL to check
        
    Returns:
        bool: True if accessible, False otherwise
    """
    if not url:
        return False
    
    try:
        # For local/static URLs, assume they're accessible
        if url.startswith('/static/') or url.startswith('/media/'):
            return True
        
        # Parse URL to check if it's properly formatted
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return False
        
        # If requests is available, do a quick check
        if HAS_REQUESTS:
            response = requests.head(url, timeout=3, allow_redirects=True)
            return response.status_code == 200
        else:
            # If requests is not available, assume external URLs are accessible
            # This prevents breaking the site when requests is not installed
            return True
            
    except Exception as e:
        logger.debug(f"Image accessibility check failed for {url}: {e}")
        return False


@register.inclusion_tag('main/components/safe_image.html')
def render_safe_image(image_url, alt_text="", css_class="", fallback_type="static", width="400", height="300", loading="lazy"):
    """
    Render a safe image using a template component.
    
    Args:
        image_url: The URL of the image to display
        alt_text: Alt text for accessibility
        css_class: CSS classes to apply to the image
        fallback_type: Type of fallback ('static' or 'placeholder')
        width: Width for placeholder fallback
        height: Height for placeholder fallback
        loading: Loading attribute
    
    Returns:
        Template context for rendering
    """
    context = {
        'image_url': image_url,
        'alt_text': alt_text,
        'css_class': css_class,
        'loading': loading,
        'width': width,
        'height': height,
    }
    
    if fallback_type == 'placeholder':
        context['fallback_url'] = f"https://via.placeholder.com/{width}x{height}/cccccc/666666?text=Image+Not+Found"
    else:
        context['fallback_url'] = static('assets/img/placeholder.jpg')
    
    return context


@register.simple_tag
def advanced_safe_image(image_url, alt_text="", css_class="", fallback_image="assets/img/placeholder.svg", width=None, height=None, loading="lazy", show_loading=False):
    """
    Advanced image display with loading states and better error handling.
    
    Args:
        image_url: The URL of the image to display
        alt_text: Alt text for accessibility
        css_class: CSS classes to apply to the image
        fallback_image: Path to fallback image (relative to static files)
        width: Optional width attribute
        height: Optional height attribute
        loading: Loading attribute (lazy, eager, auto)
        show_loading: Whether to show loading spinner
    
    Returns:
        HTML with advanced image handling
    """
    if not image_url:
        final_url = static(fallback_image)
        size_attrs = ""
        if width:
            size_attrs += f' width="{width}"'
        if height:
            size_attrs += f' height="{height}"'
        
        return mark_safe(f'<img src="{final_url}" alt="{alt_text}" class="{css_class}" loading="{loading}"{size_attrs} />')
    
    fallback_url = static(fallback_image)
    size_attrs = ""
    if width:
        size_attrs += f' width="{width}"'
    if height:
        size_attrs += f' height="{height}"'
    
    # Generate unique ID for this image
    import hashlib
    image_id = hashlib.md5(image_url.encode()).hexdigest()[:8]
    
    html = f'''
    <div class="image-container" id="container-{image_id}">
        {f'<div class="image-loading-spinner" id="spinner-{image_id}"></div>' if show_loading else ''}
        <img src="{image_url}" 
             alt="{alt_text}" 
             class="{css_class}" 
             loading="{loading}"
             {size_attrs}
             onload="if(document.getElementById('spinner-{image_id}')) document.getElementById('spinner-{image_id}').style.display='none';"
             onerror="this.src='{fallback_url}'; this.onerror=null; if(document.getElementById('spinner-{image_id}')) document.getElementById('spinner-{image_id}').style.display='none';" />
    </div>
    '''
    
    return mark_safe(html)


@register.filter
def image_or_placeholder(image_url, placeholder_type="default"):
    """
    Filter to return image URL or placeholder based on availability.
    
    Args:
        image_url: The image URL to check
        placeholder_type: Type of placeholder ('default', 'team', 'event')
    
    Returns:
        Valid image URL or placeholder URL
    """
    if not image_url:
        if placeholder_type == "team":
            return static('assets/img/team-placeholder.svg')
        elif placeholder_type == "event":
            return "https://via.placeholder.com/400x300/cccccc/666666?text=Event+Image"
        else:
            return static('assets/img/placeholder.svg')
    
    # For now, return the original URL - in production you might want to validate it
    return image_url