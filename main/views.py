from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from .models import *
from .forms import ContactForm
from .services.instagram_service import instagram_service
from django.contrib import messages
import json

def Index(request):
    # Collect all models that need to be passed to the template
    context = {
        # Hero Section
        'hero': HeroSectionText.objects.first(),
        
        # About Section
        'about_section': AboutSection.objects.first(),
        
        # Mission Section
        'mission': MissionTitleText.objects.first(),
        'missionTexts': MissionText.objects.order_by("index"),
        
        # Team Section
        'founding_members': TeamMemberTitleText.objects.first(),
        'team_members': TeamMember.objects.order_by("index"),
        
        # Events Section
        'titleEvent': EventTitleText.objects.first(),
        'events': UpcomingEvents.objects.filter(active=True),
        
        # Tech Section
        'tech_title_section': TechTitleText.objects.first(),
        'techMissionText': TechMissionText.objects.order_by("index"),
        
        # Hackathon Section
        'hackathon': HackathonText.objects.first(),
        
        # Contact Section
        'contact': ContactText.objects.first(),
        
        # Footer Section
        'footer': FooterText.objects.first(),
        
        # Instagram Section
        'instagram_config': InstagramConfig.objects.first(),
        'instagram_posts': InstagramPost.objects.filter(is_active=True)[:6],  # Limit to 6 posts
    }

    return render(request, "main/index.html", context)


def error_404(request, exception):
    context = {
        "page_title": "Error 404",
        'request': request.get_full_path(),
        'path': str(request.path)[4:-1],
    }
    return render(request, 'main/404.html', context)


import socket

def get_client_ip(request):
    """Extract the real IP address of the client."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_device_name(ip):
    """Attempt to resolve the device's hostname (if possible)."""
    try:
        hostname = socket.gethostbyaddr(ip)[0]  # Get device name
    except socket.herror:
        hostname = "Unknown Device"
    return hostname

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)

            # Get IP Address
            ip_address = get_client_ip(request)
            contact.ip_address = ip_address

            # Get Device Name (From JavaScript & Reverse Lookup)
            js_device_name = request.POST.get("device_name", "Unknown Device")
            resolved_device_name = get_device_name(ip_address)
            contact.device_name = f"{js_device_name} | {resolved_device_name}"

            # Get Browser Info
            contact.browser_info = request.META.get('HTTP_USER_AGENT', 'Unknown')

            contact.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')
    else:
        form = ContactForm()

    # Get contact section data for the template
    context = {
        'form': form,
        'contact': ContactText.objects.first(),
    }

    return render(request, 'main/contact.html', context)


def robots_txt(request):
    """
    Generate robots.txt with proper crawling directives for SEO optimization.
    Allows all crawlers to access the site and points to the sitemap.
    """
    lines = [
        "User-agent: *",
        "Allow: /",
        "",
        "# Disallow admin and private areas",
        "Disallow: /admin/",
        "Disallow: /media/private/",
        "",
        "# Sitemap location",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
        "",
        "# Crawl-delay for respectful crawling",
        "Crawl-delay: 1",
    ]
    return HttpResponse('\n'.join(lines), content_type="text/plain")

@require_http_methods(["GET"])
def test_instagram_embed(request):
    """
    Test view for Instagram embed functionality
    """
    post_url = request.GET.get('url')
    if not post_url:
        return JsonResponse({
            'error': 'Please provide a URL parameter with an Instagram post URL'
        }, status=400)
    
    try:
        embed_data = instagram_service.get_embed_data(post_url, use_cache=False)
        return JsonResponse(embed_data)
    except Exception as e:
        return JsonResponse({
            'error': f'Failed to get embed data: {str(e)}'
        }, status=500)


@require_http_methods(["POST"])
@csrf_exempt
def validate_instagram_url(request):
    """
    AJAX endpoint to validate Instagram URL
    """
    try:
        data = json.loads(request.body)
        post_url = data.get('url')
        
        if not post_url:
            return JsonResponse({
                'valid': False,
                'error': 'URL is required'
            })
        
        is_valid = instagram_service.is_valid_instagram_url(post_url)
        
        if is_valid:
            # Also try to validate the post content
            is_valid, error_message = instagram_service.validate_post_content(post_url)
            return JsonResponse({
                'valid': is_valid,
                'error': error_message if not is_valid else None
            })
        else:
            return JsonResponse({
                'valid': False,
                'error': 'Invalid Instagram URL format'
            })
            
    except json.JSONDecodeError:
        return JsonResponse({
            'valid': False,
            'error': 'Invalid JSON data'
        })
    except Exception as e:
        return JsonResponse({
            'valid': False,
            'error': f'Validation error: {str(e)}'
        })


def instagram_preview(request):
    """
    Preview page for Instagram embeds
    """
    posts = InstagramPost.objects.filter(is_active=True)[:6]
    config = InstagramConfig.objects.first()
    
    context = {
        'posts': posts,
        'config': config,
        'page_title': 'Instagram Preview'
    }
    
    return render(request, 'main/instagram_preview.html', context)


@staff_member_required
def instagram_post_preview(request, post_id):
    """
    Preview a specific Instagram post for admin
    """
    post = get_object_or_404(InstagramPost, pk=post_id)
    config = InstagramConfig.objects.first()
    
    context = {
        'post': post,
        'config': config,
        'page_title': f'Preview: Instagram Post {post.id}',
        'is_preview': True
    }
    
    return render(request, 'main/instagram_post_preview.html', context)


@staff_member_required
def instagram_quick_add(request):
    """
    Quick add form for Instagram posts
    """
    from .forms import InstagramPostQuickAddForm
    
    if request.method == 'POST':
        form = InstagramPostQuickAddForm(request.POST)
        if form.is_valid():
            post = form.save()
            messages.success(request, f'Instagram post #{post.id} added successfully!')
            
            # Redirect to preview if requested
            if 'preview' in request.POST:
                return redirect('instagram_post_preview', post_id=post.id)
            else:
                return redirect('instagram_quick_add')
    else:
        form = InstagramPostQuickAddForm()
    
    # Get recent posts for reference
    recent_posts = InstagramPost.objects.order_by('-created_at')[:5]
    
    context = {
        'form': form,
        'recent_posts': recent_posts,
        'page_title': 'Quick Add Instagram Post'
    }
    
    return render(request, 'main/instagram_quick_add.html', context)


@require_http_methods(["POST"])
@csrf_exempt
def refresh_instagram_post(request):
    """
    API endpoint to refresh Instagram post embed data
    """
    try:
        data = json.loads(request.body)
        post_url = data.get('post_url')
        
        if not post_url:
            return JsonResponse({
                'success': False,
                'error': 'Post URL is required'
            }, status=400)
        
        # Clear cache for this post
        instagram_service.clear_cache(post_url)
        
        # Try to fetch fresh data
        embed_data = instagram_service.get_embed_data(post_url, use_cache=False)
        
        return JsonResponse({
            'success': embed_data['success'],
            'error': embed_data.get('error') if not embed_data['success'] else None,
            'refreshed': True
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Refresh error: {str(e)}'
        }, status=500)