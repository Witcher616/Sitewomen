from django.contrib.sitemaps import Sitemap

from .models import Women


class PostSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.9

    def items(self):
        return Women.published.all()

    def lastmod(self, obj: Women):
        return obj.time_update
