from django.utils.translation import get_language
from django.conf import settings
from .models import HeroSectionText


def seo_context(request):
    """
    Context processor to provide SEO meta tags data for all templates.
    Provides multilingual meta titles, descriptions, and Open Graph tags.
    """
    # Get current language - this will be overridden by template's get_current_language
    current_language = get_language() or 'en'
    
    # Get hero section for dynamic content
    hero = HeroSectionText.objects.first()
    
    # Default SEO data structure
    seo_data = {
        'site_name': 'TUM Albanian Society',
        'site_url': request.build_absolute_uri('/'),
        'default_image': request.build_absolute_uri('/static/assets/img/logowithtext.png'),
        'twitter_handle': '@albanian_students_tum',
        'facebook_app_id': '',  # Add if available
        'author': 'TUM Albanian Society',
        'robots': 'index, follow',
        'theme_color': '#1a1a1a',
        'application_name': 'TUM Albanian Society',
    }
    
    # Language-specific SEO content
    if current_language == 'sq':
        seo_data.update({
            'meta_title': hero.title_sq if hero else 'Shoqata e Studentëve Shqiptarë TUM',
            'meta_description': hero.description_sq if hero else 'Lidhja e studentëve shqiptarë dhe promovimi i shkëmbimit kulturor në Universitetin Teknik të Mynihut',
            'meta_keywords': 'studentë shqiptarë, TUM, Universiteti Teknik München, shoqata studentore, shkëmbim kulturor, Shqipëri, Gjermani',
            'og_title': hero.title_sq if hero else 'Shoqata e Studentëve Shqiptarë TUM',
            'og_description': hero.subtitle_sq if hero else 'Bashkohuni me komunitetin tonë të studentëve shqiptarë në TUM',
        })
    elif current_language == 'de':
        seo_data.update({
            'meta_title': hero.title_de if hero else 'TUM Albanische Studentenvereinigung',
            'meta_description': hero.description_de if hero else 'Verbindung albanischer Studenten und Förderung des kulturellen Austauschs an der Technischen Universität München',
            'meta_keywords': 'albanische Studenten, TUM, Technische Universität München, Studentenvereinigung, kultureller Austausch, Albanien, Deutschland',
            'og_title': hero.title_de if hero else 'TUM Albanische Studentenvereinigung',
            'og_description': hero.subtitle_de if hero else 'Treten Sie unserer Gemeinschaft albanischer Studenten an der TUM bei',
        })
    else:  # English (default)
        seo_data.update({
            'meta_title': hero.title_en if hero else 'TUM Albanian Society - Albanian Students at Technical University of Munich',
            'meta_description': hero.description_en if hero else 'Connecting Albanian students and promoting cultural exchange at the Technical University of Munich',
            'meta_keywords': 'Albanian students, TUM, Technical University Munich, student society, cultural exchange, Albania, Germany',
            'og_title': hero.title_en if hero else 'TUM Albanian Society',
            'og_description': hero.subtitle_en if hero else 'Join our community of Albanian students at TUM',
        })
    
    # Add current language and canonical URL
    seo_data.update({
        'current_language': current_language,
        'canonical_url': request.build_absolute_uri(),
        'alternate_languages': [
            {'code': 'en', 'url': request.build_absolute_uri().replace(f'/{current_language}/', '/en/') if current_language != 'en' else request.build_absolute_uri()},
            {'code': 'sq', 'url': request.build_absolute_uri().replace(f'/{current_language}/', '/sq/') if current_language != 'sq' else request.build_absolute_uri()},
            {'code': 'de', 'url': request.build_absolute_uri().replace(f'/{current_language}/', '/de/') if current_language != 'de' else request.build_absolute_uri()},
        ]
    })
    
    # Add breadcrumb data for structured data
    breadcrumb_data = {
        'breadcrumb_home': [
            {'name': 'Home' if current_language == 'en' else ('Kreu' if current_language == 'sq' else 'Startseite'), 'url': request.build_absolute_uri()}
        ],
        'breadcrumb_contact': [
            {'name': 'Home' if current_language == 'en' else ('Kreu' if current_language == 'sq' else 'Startseite'), 'url': seo_data['site_url']},
            {'name': 'Contact' if current_language == 'en' else ('Kontakt' if current_language == 'sq' else 'Kontakt'), 'url': request.build_absolute_uri()}
        ]
    }
    
    return {'seo': seo_data, **breadcrumb_data}