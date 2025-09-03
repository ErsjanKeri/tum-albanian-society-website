from django.contrib import admin
from django.urls import path, include 

from . import views 
from .views import contact_view, robots_txt, test_instagram_embed, validate_instagram_url, instagram_preview, instagram_post_preview, instagram_quick_add, refresh_instagram_post
from django.shortcuts import render
from .models import InstagramConfig, InstagramPost



urlpatterns = [
    path('', views.Index, name = 'index'),
	path('contact/', contact_view, name='contact'),
    path('robots.txt', robots_txt, name='robots_txt'),
    
    # Instagram testing endpoints
    path('test/instagram-embed/', test_instagram_embed, name='test_instagram_embed'),
    path('api/validate-instagram-url/', validate_instagram_url, name='validate_instagram_url'),
    path('api/refresh-instagram-post/', refresh_instagram_post, name='refresh_instagram_post'),
    path('instagram-preview/', instagram_preview, name='instagram_preview'),
    
    # Instagram admin endpoints
    path('admin/instagram/post/<int:post_id>/preview/', instagram_post_preview, name='instagram_post_preview'),
    path('admin/instagram/quick-add/', instagram_quick_add, name='instagram_quick_add'),
]
