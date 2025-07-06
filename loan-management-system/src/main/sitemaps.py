from django.contrib import sitemaps
from django.urls import reverse


class HomeViewSitemap(sitemaps.Sitemap):
    priority = 1
    changefreq = "daily"

    def items(self):
        return ["main:home", ]

    def location(self, item):
        return reverse(item)


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = "monthly"

    def items(self):
        return ["main:about", "main:contact", "main:privacy"]

    def location(self, item):
        return reverse(item)
