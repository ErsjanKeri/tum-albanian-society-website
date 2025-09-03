from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import get_language

register = template.Library()


@register.simple_tag(takes_context=True)
def page_title(context, title=None):
    """
    Generate page title with site name.
    Usage: {% page_title "Custom Page Title" %}
    """
    seo = context.get('seo', {})
    site_name = seo.get('site_name', 'TUM Albanian Society')
    
    if title:
        return f"{title} | {site_name}"
    return seo.get('meta_title', site_name)


@register.simple_tag(takes_context=True)
def page_description(context, description=None):
    """
    Generate page description.
    Usage: {% page_description "Custom page description" %}
    """
    if description:
        return description
    
    seo = context.get('seo', {})
    return seo.get('meta_description', '')


@register.simple_tag(takes_context=True)
def og_image(context, image_url=None):
    """
    Generate Open Graph image URL.
    Usage: {% og_image "/static/custom-image.jpg" %}
    """
    if image_url:
        request = context.get('request')
        if request:
            return request.build_absolute_uri(image_url)
        return image_url
    
    seo = context.get('seo', {})
    return seo.get('default_image', '')


@register.inclusion_tag('main/seo_meta.html', takes_context=True)
def seo_meta(context, title=None, description=None, image=None, keywords=None, og_type=None):
    """
    Include SEO meta tags with optional overrides.
    Usage: {% seo_meta title="Custom Title" description="Custom Description" og_type="article" %}
    """
    seo = context.get('seo', {})
    request = context.get('request')
    
    # Override defaults with provided values
    meta_data = {
        'title': title or seo.get('meta_title', ''),
        'description': description or seo.get('meta_description', ''),
        'keywords': keywords or seo.get('meta_keywords', ''),
        'image': image or seo.get('default_image', ''),
        'url': request.build_absolute_uri() if request else '',
        'og_type': og_type or 'website',
    }
    
    # Ensure image is absolute URL
    if meta_data['image'] and request and not meta_data['image'].startswith('http'):
        meta_data['image'] = request.build_absolute_uri(meta_data['image'])
    
    return {
        'seo': seo,
        'meta': meta_data,
        'request': request,
    }


@register.simple_tag
def hreflang_code(language_code):
    """
    Convert Django language code to proper hreflang format.
    Usage: {% hreflang_code "sq" %}
    """
    mapping = {
        'sq': 'sq-AL',
        'en': 'en-US', 
        'de': 'de-DE',
    }
    return mapping.get(language_code, language_code)


@register.simple_tag(takes_context=True)
def breadcrumb_schema(context, items):
    """
    Generate breadcrumb structured data.
    Usage: {% breadcrumb_schema breadcrumb_items %}
    """
    import json
    
    if not items:
        return ''
    
    breadcrumb_list = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": []
    }
    
    for index, item in enumerate(items, 1):
        breadcrumb_list["itemListElement"].append({
            "@type": "ListItem",
            "position": index,
            "name": item.get('name', ''),
            "item": item.get('url', '')
        })
    
    return mark_safe(f'<script type="application/ld+json">{json.dumps(breadcrumb_list, ensure_ascii=False)}</script>')


@register.simple_tag(takes_context=True)
def webpage_schema(context, page_type="WebPage"):
    """
    Generate WebPage structured data.
    Usage: {% webpage_schema "ContactPage" %}
    """
    import json
    
    seo = context.get('seo', {})
    request = context.get('request')
    
    if not request:
        return ''
    
    webpage_data = {
        "@context": "https://schema.org",
        "@type": page_type,
        "name": seo.get('meta_title', ''),
        "description": seo.get('meta_description', ''),
        "url": request.build_absolute_uri(),
        "inLanguage": get_language() or 'en',
        "isPartOf": {
            "@type": "WebSite",
            "name": seo.get('site_name', ''),
            "url": seo.get('site_url', '')
        }
    }
    
    return mark_safe(f'<script type="application/ld+json">{json.dumps(webpage_data, ensure_ascii=False)}</script>')


@register.simple_tag(takes_context=True)
def event_schema(context, event):
    """
    Generate Event structured data for individual events.
    Usage: {% event_schema event_object %}
    """
    import json
    from django.utils import timezone
    
    if not event:
        return ''
    
    seo = context.get('seo', {})
    request = context.get('request')
    current_language = get_language() or 'en'
    
    # Get event details based on current language
    if current_language == 'sq':
        event_name = getattr(event, 'title_sq', '') or getattr(event, 'title_en', '')
        event_description = getattr(event, 'content_sq', '') or getattr(event, 'content_en', '')
    elif current_language == 'de':
        event_name = getattr(event, 'title_de', '') or getattr(event, 'title_en', '')
        event_description = getattr(event, 'content_de', '') or getattr(event, 'content_en', '')
    else:
        event_name = getattr(event, 'title_en', '')
        event_description = getattr(event, 'content_en', '')
    
    # Create event date from day, month, year fields
    try:
        event_date = timezone.datetime(
            year=getattr(event, 'year', timezone.now().year),
            month=getattr(event, 'month', 1),
            day=getattr(event, 'day', 1)
        ).isoformat()
    except:
        event_date = timezone.now().isoformat()
    
    event_data = {
        "@context": "https://schema.org",
        "@type": "Event",
        "name": event_name,
        "description": event_description,
        "startDate": event_date,
        "eventStatus": "https://schema.org/EventScheduled",
        "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
        "location": {
            "@type": "Place",
            "name": "Technical University of Munich",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "Arcisstraße 21",
                "addressLocality": "Munich",
                "addressRegion": "Bavaria",
                "postalCode": "80333",
                "addressCountry": "DE"
            }
        },
        "organizer": {
            "@type": "Organization",
            "name": seo.get('site_name', 'TUM Albanian Society'),
            "url": seo.get('site_url', ''),
            "sameAs": [
                "https://www.instagram.com/albanian_students_tum",
                "https://www.facebook.com/albanianstudents.tum"
            ]
        },
        "offers": {
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "EUR",
            "availability": "https://schema.org/InStock",
            "url": request.build_absolute_uri() if request else seo.get('site_url', '')
        }
    }
    
    return mark_safe(f'<script type="application/ld+json">{json.dumps(event_data, ensure_ascii=False)}</script>')


@register.simple_tag(takes_context=True)
def events_list_schema(context, events):
    """
    Generate EventSeries structured data for multiple events.
    Usage: {% events_list_schema events_queryset %}
    """
    import json
    from django.utils import timezone
    
    if not events:
        return ''
    
    seo = context.get('seo', {})
    request = context.get('request')
    current_language = get_language() or 'en'
    
    events_list = []
    for event in events:
        # Get event details based on current language
        if current_language == 'sq':
            event_name = getattr(event, 'title_sq', '') or getattr(event, 'title_en', '')
            event_description = getattr(event, 'content_sq', '') or getattr(event, 'content_en', '')
        elif current_language == 'de':
            event_name = getattr(event, 'title_de', '') or getattr(event, 'title_en', '')
            event_description = getattr(event, 'content_de', '') or getattr(event, 'content_en', '')
        else:
            event_name = getattr(event, 'title_en', '')
            event_description = getattr(event, 'content_en', '')
        
        # Create event date
        try:
            event_date = timezone.datetime(
                year=getattr(event, 'year', timezone.now().year),
                month=getattr(event, 'month', 1),
                day=getattr(event, 'day', 1)
            ).isoformat()
        except:
            event_date = timezone.now().isoformat()
        
        events_list.append({
            "@type": "Event",
            "name": event_name,
            "description": event_description,
            "startDate": event_date,
            "eventStatus": "https://schema.org/EventScheduled",
            "location": {
                "@type": "Place",
                "name": "Technical University of Munich",
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": "Arcisstraße 21",
                    "addressLocality": "Munich",
                    "postalCode": "80333",
                    "addressCountry": "DE"
                }
            }
        })
    
    events_data = {
        "@context": "https://schema.org",
        "@type": "EventSeries",
        "name": "TUM Albanian Society Events",
        "description": "Regular events organized by the Albanian Society at Technical University of Munich",
        "organizer": {
            "@type": "Organization",
            "name": seo.get('site_name', 'TUM Albanian Society'),
            "url": seo.get('site_url', '')
        },
        "subEvent": events_list
    }
    
    return mark_safe(f'<script type="application/ld+json">{json.dumps(events_data, ensure_ascii=False)}</script>')


@register.simple_tag(takes_context=True)
def person_schema(context, person):
    """
    Generate Person structured data for team members.
    Usage: {% person_schema team_member %}
    """
    import json
    
    if not person:
        return ''
    
    seo = context.get('seo', {})
    current_language = get_language() or 'en'
    
    # Get person details based on current language
    if current_language == 'sq':
        person_description = getattr(person, 'description_sq', '') or getattr(person, 'description_en', '')
        person_field = getattr(person, 'field_sq', '') or getattr(person, 'field_en', '')
    elif current_language == 'de':
        person_description = getattr(person, 'description_de', '') or getattr(person, 'description_en', '')
        person_field = getattr(person, 'field_de', '') or getattr(person, 'field_en', '')
    else:
        person_description = getattr(person, 'description_en', '')
        person_field = getattr(person, 'field_en', '')
    
    person_data = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": getattr(person, 'name', ''),
        "description": person_description,
        "jobTitle": person_field,
        "memberOf": {
            "@type": "Organization",
            "name": seo.get('site_name', 'TUM Albanian Society'),
            "url": seo.get('site_url', '')
        },
        "affiliation": {
            "@type": "Organization",
            "name": "Technical University of Munich",
            "url": "https://www.tum.de"
        }
    }
    
    # Add image if available
    if hasattr(person, 'image') and person.image:
        person_data["image"] = {
            "@type": "ImageObject",
            "url": person.image.url if hasattr(person.image, 'url') else str(person.image),
            "caption": f"Photo of {person.name}"
        }
    
    return mark_safe(f'<script type="application/ld+json">{json.dumps(person_data, ensure_ascii=False)}</script>')


@register.simple_tag(takes_context=True)
def optimized_image(context, image_url, alt_text="", css_class="", loading="lazy", fallback_url="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='300' viewBox='0 0 400 300'%3E%3Crect width='400' height='300' fill='%23f0f0f0'/%3E%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' font-family='Arial, sans-serif' font-size='16' fill='%23666'%3EImage not available%3C/text%3E%3C/svg%3E"):
    """
    Generate optimized image tag with fallback support and proper attributes.
    Usage: {% optimized_image image_url "Alt text" "css-class" "lazy" %}
    """
    if not image_url:
        image_url = fallback_url
    
    # Build image attributes
    attributes = []
    if css_class:
        attributes.append(f'class="{css_class}"')
    if loading:
        attributes.append(f'loading="{loading}"')
    if alt_text:
        attributes.append(f'alt="{alt_text}"')
    else:
        attributes.append('alt=""')
    
    # Add error handling for broken images
    onerror_js = f'this.onerror=null; this.src="{fallback_url}";'
    attributes.append(f'onerror="{onerror_js}"')
    
    attributes_str = ' '.join(attributes)
    
    return mark_safe(f'<img src="{image_url}" {attributes_str} />')


@register.simple_tag
def responsive_image(image_url, alt_text="", css_class="img-fluid", sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"):
    """
    Generate responsive image with proper sizing attributes.
    Usage: {% responsive_image image_url "Alt text" "css-class" %}
    """
    fallback_url = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='300' viewBox='0 0 400 300'%3E%3Crect width='400' height='300' fill='%23f0f0f0'/%3E%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' font-family='Arial, sans-serif' font-size='16' fill='%23666'%3EImage not available%3C/text%3E%3C/svg%3E"
    if not image_url:
        image_url = fallback_url
    
    # For now, we'll use the single image URL, but this can be extended
    # to support multiple image sizes when using a CDN or image service
    attributes = [
        f'src="{image_url}"',
        f'alt="{alt_text}"',
        f'class="{css_class}"',
        'loading="lazy"',
        f'sizes="{sizes}"',
        f'onerror="this.onerror=null; this.src=\'{fallback_url}\';"'
    ]
    
    return mark_safe(f'<img {" ".join(attributes)} />')


@register.simple_tag(takes_context=True)
def team_schema(context, team_members):
    """
    Generate Organization with members structured data for the team section.
    Usage: {% team_schema team_members_queryset %}
    """
    import json
    
    if not team_members:
        return ''
    
    seo = context.get('seo', {})
    current_language = get_language() or 'en'
    
    members_list = []
    for member in team_members:
        # Get member details based on current language
        if current_language == 'sq':
            member_description = getattr(member, 'description_sq', '') or getattr(member, 'description_en', '')
            member_field = getattr(member, 'field_sq', '') or getattr(member, 'field_en', '')
        elif current_language == 'de':
            member_description = getattr(member, 'description_de', '') or getattr(member, 'description_en', '')
            member_field = getattr(member, 'field_de', '') or getattr(member, 'field_en', '')
        else:
            member_description = getattr(member, 'description_en', '')
            member_field = getattr(member, 'field_en', '')
        
        member_data = {
            "@type": "Person",
            "name": getattr(member, 'name', ''),
            "description": member_description,
            "jobTitle": member_field
        }
        
        # Add image if available
        if hasattr(member, 'image') and member.image:
            member_data["image"] = {
                "@type": "ImageObject",
                "url": member.image.url if hasattr(member.image, 'url') else str(member.image),
                "caption": f"Photo of {member.name}"
            }
        
        members_list.append(member_data)
    
    team_data = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "@id": seo.get('site_url', '') + "#team",
        "name": seo.get('site_name', 'TUM Albanian Society') + " Team",
        "description": "Founding members and team of the Albanian Society at Technical University of Munich",
        "parentOrganization": {
            "@type": "Organization",
            "name": seo.get('site_name', 'TUM Albanian Society'),
            "url": seo.get('site_url', '')
        },
        "member": members_list
    }
    
    return mark_safe(f'<script type="application/ld+json">{json.dumps(team_data, ensure_ascii=False)}</script>')