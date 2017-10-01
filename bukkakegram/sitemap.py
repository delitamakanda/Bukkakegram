import datetime
from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from bukkakegram.models import Bukkake

class BukkakeSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Bukkake.objects.order_by('-id')[:10]

    def lastmod(self, obj):
        return obj.created_date
