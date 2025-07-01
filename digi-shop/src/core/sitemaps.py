from django.urls import reverse
from django.contrib import sitemaps


class HomeViewSitemap(sitemaps.Sitemap):
    priority = 1
    changefreq = "daily"

    def items(self):
        return ["shop:home", ]

    def location(self, item):
        return reverse(item)


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = "monthly"

    def items(self):
        return ["shop:about", "shop:contact"]

    def location(self, item):
        return reverse(item)
