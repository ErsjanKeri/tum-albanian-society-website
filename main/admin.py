from django.contrib import admin
from django.utils.html import format_html
from django.db import models
from .models import *
from .forms import InstagramPostAdminForm


# change admin page name from Django Administration to Admin Panel
admin.site.site_header = "TUM Alb Society Admin"
admin.site.site_title = "TUM Alb Society Admin"
admin.site.index_title = "Welcome to TUM Alb Society Admin Panel"
# change the color of the styling of the admin panel


# HERO SECTION
@admin.register(HeroSectionText)
class HeroSectionTextAdmin(admin.ModelAdmin):
    list_display = ("title_en", "title_sq", "title_de")
    

# ABOUT US SECTION
admin.site.register(AboutSection)


# MISSION SECTION
admin.site.register(MissionText)
admin.site.register(MissionTitleText)

# TEAM SECTION
@admin.register(TeamMemberTitleText)
class FoundingMembersTextAdmin(admin.ModelAdmin):
    list_display = ('title_sq', 'title_en', 'title_de')
    search_fields = ('title_sq', 'title_en', 'title_de')
    
@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('index', 'name', 'field_en', 'profile_image_url')
    ordering = ('index',)
    fields = ('index', 'name', ('field_sq', 'field_en', 'field_de'), 
              ('description_sq', 'description_en', 'description_de'), 'profile_image_url')
    search_fields = ('name', 'field_en', 'field_sq', 'field_de')



# EVENT SECTION
admin.site.register(EventTitleText)

@admin.register(UpcomingEvents)
class UpcomingEventsAdmin(admin.ModelAdmin):
    list_display = ('year', 'month', 'day', 'title_en', 'active')
    list_filter = ('year', 'month', 'active')
    search_fields = ('title_en', 'title_sq', 'title_de')
    ordering = ('year', 'month', 'day')
    list_editable = ('active',)


# TECH SECTION
admin.site.register(TechTitleText)
admin.site.register(TechMissionText)
admin.site.register(HackathonText)


# CONTACT US SECTION
@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')
    
admin.site.register(ContactText)

# FOOTER SECTION
admin.site.register(FooterText)


# INSTAGRAM SECTION
@admin.register(InstagramPost)
class InstagramPostAdmin(admin.ModelAdmin):
    form = InstagramPostAdminForm
    list_display = ('id', 'caption_preview', 'post_type', 'media_count', 'post_link', 'display_order', 'is_active', 'created_at')
    list_filter = ('is_active', 'post_type', 'created_at')
    search_fields = ('caption', 'post_url')
    ordering = ('display_order', '-created_at')
    list_editable = ('display_order', 'is_active')
    
    def caption_preview(self, obj):
        """Show a preview of the caption in the admin list"""
        if obj.caption:
            return obj.caption[:50] + "..." if len(obj.caption) > 50 else obj.caption
        return "No caption"
    caption_preview.short_description = "Caption Preview"
    
    def post_link(self, obj):
        """Show a link to the Instagram post"""
        if obj.post_url:
            return format_html(
                '<a href="{}" target="_blank" rel="noopener noreferrer" style="color: #E50914;">View on Instagram</a>',
                obj.post_url
            )
        return "No URL"
    post_link.short_description = "Instagram Link"
    
    def media_count(self, obj):
        """Show the number of media items"""
        count = obj.get_media_count()
        if count > 1:
            return format_html('<span style="color: #E50914; font-weight: bold;">{} images</span>', count)
        elif count == 1:
            return "1 image"
        else:
            return "No media"
    media_count.short_description = "Media Count"
    
    fieldsets = (
        ('Post Content', {
            'fields': ('post_url', 'caption', 'post_type'),
            'description': 'Enter the Instagram post URL and basic information.'
        }),
        ('Media URLs', {
            'fields': ('primary_media_url', 'media_urls_text'),
            'description': 'Add media URLs. For carousel posts, enter multiple URLs (one per line). The first URL will be used as the primary image.'
        }),
        ('Display Settings', {
            'fields': ('display_order', 'is_active'),
            'description': 'Control how and where this post appears on the website.'
        }),
    )
    
    def response_add(self, request, obj, post_url_continue=None):
        """Handle Save & Preview button"""
        if "_preview" in request.POST:
            from django.shortcuts import redirect
            return redirect('instagram_post_preview', post_id=obj.pk)
        return super().response_add(request, obj, post_url_continue)
    
    def response_change(self, request, obj):
        """Handle Save & Preview button"""
        if "_preview" in request.POST:
            from django.shortcuts import redirect
            return redirect('instagram_post_preview', post_id=obj.pk)
        return super().response_change(request, obj)


@admin.register(InstagramConfig)
class InstagramConfigAdmin(admin.ModelAdmin):
    list_display = ('posts_per_page', 'show_captions', 'max_caption_length', 'is_active')
    actions = ['fetch_instagram_posts']
    
    fieldsets = (
        ('Display Settings', {
            'fields': ('posts_per_page', 'show_captions', 'max_caption_length', 'is_active')
        }),
        ('Section Titles', {
            'fields': ('section_title_sq', 'section_title_en', 'section_title_de')
        }),
    )
    
    def fetch_instagram_posts(self, request, queryset):
        """Fetch latest Instagram posts from @albanian_students_tum"""
        try:
            from django.core.management import call_command
            call_command('curate_albanian_students_posts', '--auto-fetch')
            self.message_user(request, 'Successfully fetched Instagram posts from @albanian_students_tum')
        except Exception as e:
            self.message_user(request, f'Error fetching Instagram posts: {str(e)}', level='ERROR')
    
    fetch_instagram_posts.short_description = "🔄 Fetch Latest Instagram Posts"
    
    def has_add_permission(self, request):
        # Only allow one configuration instance
        return not InstagramConfig.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion of the configuration
        return False
