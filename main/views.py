from django.shortcuts import render, redirect
from .models import *
from .forms import ContactForm
from django.contrib import messages

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

    return render(request, 'main/index.html', {'form': form})