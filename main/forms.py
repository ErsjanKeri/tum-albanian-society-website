from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from .models import ContactUs, InstagramPost
from .services.instagram_service import instagram_service


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Your Message'}),
        }


class InstagramPostAdminForm(forms.ModelForm):
    """Custom form for Instagram post admin with validation"""
    
    # Additional field for easier media URL input
    media_urls_text = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Enter media URLs, one per line:\nhttps://example.com/image1.jpg\nhttps://example.com/image2.jpg\nhttps://example.com/image3.jpg',
            'style': 'font-family: monospace; font-size: 12px;'
        }),
        label="Media URLs (one per line)",
        help_text="Enter multiple image URLs for carousel posts, one URL per line"
    )
    
    class Meta:
        model = InstagramPost
        fields = '__all__'
        widgets = {
            'caption': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Enter the Instagram post caption...'
            }),
            'primary_media_url': forms.URLInput(attrs={
                'placeholder': 'https://example.com/main-image.jpg'
            }),
            'post_url': forms.URLInput(attrs={
                'placeholder': 'https://www.instagram.com/p/ABC123/'
            }),
            'post_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'media_urls': forms.HiddenInput(),  # Hide the JSON field
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Populate media_urls_text from existing data
        if self.instance and self.instance.pk and hasattr(self.instance, 'media_urls') and self.instance.media_urls:
            try:
                urls = self.instance.get_all_media_urls()
                if urls:
                    self.fields['media_urls_text'].initial = '\n'.join(urls)
            except (AttributeError, TypeError):
                # Handle cases where media_urls might not be properly formatted
                pass
    
    def clean_post_url(self):
        """Validate Instagram post URL"""
        post_url = self.cleaned_data.get('post_url')
        
        if not post_url:
            raise ValidationError('Instagram post URL is required.')
        
        # Validate URL format
        if not instagram_service.is_valid_instagram_url(post_url):
            raise ValidationError(
                'Please enter a valid Instagram post URL. '
                'Supported formats: instagram.com/p/..., instagram.com/reel/..., instagram.com/tv/...'
            )
        
        return post_url
    
    def clean_media_urls_text(self):
        """Validate and parse media URLs from text input"""
        media_urls_text = self.cleaned_data.get('media_urls_text', '')
        
        if not media_urls_text or not str(media_urls_text).strip():
            return []
        
        urls = []
        raw_text = str(media_urls_text).strip()
        
        try:
            # First try to split by newlines
            lines = raw_text.split('\n')
            
            # If we only get one line, try to extract URLs using regex
            if len(lines) == 1:
                import re
                
                # Enhanced pattern specifically for Instagram CDN URLs
                # This pattern looks for Instagram CDN URLs that end with _nc_sid parameter
                instagram_cdn_pattern = r'https://scontent-[^.]+\.cdninstagram\.com/[^?]+\?[^&]*&_nc_sid=[a-f0-9]+'
                found_urls = re.findall(instagram_cdn_pattern, raw_text)
                
                if not found_urls:
                    # Fallback pattern for general Instagram CDN URLs
                    general_pattern = r'https://[^h\s]*cdninstagram\.com[^h\s]*(?=https://|$)'
                    found_urls = re.findall(general_pattern, raw_text)
                
                if not found_urls:
                    # More general pattern to extract any HTTPS URLs
                    url_pattern = r'https://[^h\s]*(?=https://|$)'
                    found_urls = re.findall(url_pattern, raw_text)
                
                if not found_urls:
                    # Final fallback: split by 'https://' and reconstruct
                    parts = raw_text.split('https://')
                    found_urls = []
                    for i, part in enumerate(parts):
                        if i == 0 and not part:
                            continue  # Skip empty first part
                        if part:
                            url = 'https://' + part
                            # Clean up URL - remove everything after another URL starts
                            url = re.sub(r'(https://.*?)(https://.*)', r'\1', url)
                            found_urls.append(url)
                
                if found_urls:
                    lines = found_urls
            
            for line in lines:
                url = str(line).strip()
                if url and url.startswith(('http://', 'https://')):
                    # Clean up Instagram CDN URLs
                    if 'cdninstagram.com' in url:
                        import re
                        # Remove any trailing parameters that might be concatenated
                        # Keep everything up to and including _nc_sid parameter
                        if '&_nc_sid=' in url:
                            match = re.search(r'(.*&_nc_sid=[a-f0-9]+)', url)
                            if match:
                                url = match.group(1)
                        
                        # Remove any text after the URL that doesn't belong
                        url = re.sub(r'(https://[^h]*cdninstagram\.com[^h]*).*', r'\1', url)
                    
                    if url not in urls:  # Avoid duplicates
                        urls.append(url)
            
            if not urls and raw_text:
                raise ValidationError('No valid URLs found. Please enter URLs starting with http:// or https://, one per line.')
            
        except Exception as e:
            # If there's any parsing error, return empty list and let the form handle it
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"URL parsing error: {e}")
            return []
        
        return urls
    
    def clean_primary_media_url(self):
        """Validate primary media URL if provided"""
        primary_media_url = self.cleaned_data.get('primary_media_url')
        
        if primary_media_url:
            # Basic URL validation is handled by URLField
            # Additional validation could be added here
            pass
        
        return primary_media_url
    
    def clean(self):
        """Cross-field validation"""
        cleaned_data = super().clean()
        
        try:
            post_url = cleaned_data.get('post_url')
            primary_media_url = cleaned_data.get('primary_media_url')
            media_urls_list = cleaned_data.get('media_urls_text', [])
            post_type = cleaned_data.get('post_type')
            
            # Set media_urls from parsed text
            if media_urls_list:
                cleaned_data['media_urls'] = media_urls_list
                
                # Auto-detect post type based on media count
                if len(media_urls_list) > 1:
                    cleaned_data['post_type'] = 'carousel'
                elif not post_type or post_type == 'image':
                    cleaned_data['post_type'] = 'image'
                
                # Set primary media URL if not provided
                if not primary_media_url and media_urls_list:
                    cleaned_data['primary_media_url'] = media_urls_list[0]
            
            # Skip API validation for manual posts - they should work independently
            # Manual posts with media URLs don't need API validation
            
        except Exception as e:
            # If there's any issue with form processing, log it but don't break the form
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Form validation warning: {e}")
        
        return cleaned_data


class InstagramPostQuickAddForm(forms.ModelForm):
    """Simplified form for quickly adding Instagram posts"""
    
    auto_extract_media = forms.BooleanField(
        required=False,
        initial=True,
        label="Auto-extract media URLs",
        help_text="Automatically try to extract media URLs from the Instagram post"
    )
    
    class Meta:
        model = InstagramPost
        fields = ['post_url', 'caption', 'display_order', 'is_active']
        widgets = {
            'post_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://www.instagram.com/p/ABC123/',
                'required': True,
                'style': 'font-size: 14px;'
            }),
            'caption': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional: Enter custom caption or leave empty'
            }),
            'display_order': forms.NumberInput(attrs={
                'class': 'form-control',
                'value': 0,
                'min': 0,
                'help_text': 'Lower numbers appear first'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'checked': True
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default display order to be higher than existing posts
        if not self.instance.pk:
            max_order = InstagramPost.objects.aggregate(models.Max('display_order'))['display_order__max'] or 0
            self.fields['display_order'].initial = max_order + 1
    
    def clean_post_url(self):
        """Validate Instagram post URL"""
        post_url = self.cleaned_data.get('post_url')
        
        if not instagram_service.is_valid_instagram_url(post_url):
            raise ValidationError(
                'Please enter a valid Instagram post URL. '
                'Supported formats: instagram.com/p/..., instagram.com/reel/..., instagram.com/tv/...'
            )
        
        # Check if this URL already exists
        if InstagramPost.objects.filter(post_url=post_url).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise ValidationError('A post with this URL already exists.')
        
        return post_url
    
    def save(self, commit=True):
        """Save with automatic media URL extraction if possible"""
        instance = super().save(commit=False)
        
        # Try to extract media URLs if requested and API is available
        if self.cleaned_data.get('auto_extract_media', True) and instance.post_url:
            try:
                # Only try API extraction if Instagram access token is configured
                from django.conf import settings
                access_token = getattr(settings, 'INSTAGRAM_ACCESS_TOKEN', None)
                
                if access_token:
                    # Try to get embed data to extract media information
                    embed_data = instagram_service.get_embed_data(instance.post_url, use_cache=False)
                    if embed_data.get('success'):
                        if embed_data.get('thumbnail_url') and not instance.primary_media_url:
                            instance.primary_media_url = embed_data['thumbnail_url']
                        
                        # If no caption provided, try to extract from embed
                        if not instance.caption and embed_data.get('title'):
                            # Instagram embed titles often contain captions
                            instance.caption = embed_data['title'][:2000]  # Allow up to 2000 characters
                else:
                    # No API token - skip extraction, form will work fine without it
                    pass
                        
            except Exception as e:
                # If extraction fails, continue without it - form should still work
                pass
        
        if commit:
            instance.save()
        
        return instance