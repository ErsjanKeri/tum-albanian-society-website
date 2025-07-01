from django.contrib import admin
from .models import *


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
admin.site.register(ContactInfo)
@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')
    
admin.site.register(ContactText)

# FOOTER SECTION
admin.site.register(FooterText)
