from django.contrib.sitemaps import Sitemap 
from django.urls import reverse

from .models import * 

class StaticViewsSitemap(Sitemap):
    priority = 1
    changefreq = 'monthly'
    protocol = 'https'

    def items(self):
        #return ['index', 'about', 'contact', 'offers']
        return ['index']

    def location(self, item):
        return reverse(item)
