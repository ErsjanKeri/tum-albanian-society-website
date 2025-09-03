from django.contrib import admin
from django.urls import path, include 

from django.conf.urls.static import static  
from django.conf import settings

from django.conf.urls.i18n import i18n_patterns 
from django.contrib.sitemaps.views import sitemap
from django.conf.urls import handler404

from main.sitemaps import StaticViewsSitemap, EventsSitemap
from main.views import instagram_quick_add, instagram_post_preview

handler404 = 'main.views.error_404'

sitemaps = {
	'static': StaticViewsSitemap,
    'events': EventsSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps' : sitemaps}, name = 'django.contrib.sitemaps.views.sitemap'),
    path('i18n/', include('django.conf.urls.i18n')),
    
    # Admin-specific Instagram URLs (outside i18n)
    path('admin/instagram/quick-add/', instagram_quick_add, name='instagram_quick_add'),
    path('admin/instagram/preview/<int:post_id>/', instagram_post_preview, name='instagram_post_preview'),
]

urlpatterns += i18n_patterns(
    path('', include("main.urls")),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    