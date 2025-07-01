from django.contrib import admin
from django.urls import path, include 

from django.conf.urls.static import static  
from django.conf import settings

from django.conf.urls.i18n import i18n_patterns 
from django.contrib.sitemaps.views import sitemap
from django.conf.urls import handler404

from main.sitemaps import StaticViewsSitemap

handler404 = 'main.views.error_404'

sitemaps = {
	'static' : StaticViewsSitemap
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("main.urls")),
    path('sitemap.xml', sitemap, {'sitemaps' : sitemaps}, name = 'django.contrib.sitemaps.views.sitemap'),
    
]

urlpatterns += i18n_patterns(
    path('i18n/', include('django.conf.urls.i18n')), 
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    