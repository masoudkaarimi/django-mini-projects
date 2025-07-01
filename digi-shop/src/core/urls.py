from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.urls import path, include, re_path
from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps.views import sitemap

from core.sitemaps import HomeViewSitemap, StaticViewSitemap
from apps.shop.views import NotFoundView, ForbiddenView, InternalServerErrorView

sitemaps = {
    'home': HomeViewSitemap,
    'static': StaticViewSitemap,
}

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('apps.shop.urls', namespace='shop')),
    path('', include('apps.account.urls', namespace='account')),
    path('', include('apps.checkout.urls', namespace='checkout')),
    path('', include('apps.inventory.urls', namespace='inventory')),

    path("sitemap.xml/", sitemap, {'sitemaps': sitemaps}),
    path('robots.txt/', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),

    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('django_vite_plugin.urls')),
)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [re_path(r'^rosetta/', include('rosetta.urls'))]

# Static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Error Pages
handler404 = NotFoundView.as_view()
handler403 = ForbiddenView.as_view()
handler500 = InternalServerErrorView.as_view()
