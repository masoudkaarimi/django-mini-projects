"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include, re_path, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import TemplateView
from django.conf.urls import handler404, handler403, handler500
from django.contrib.auth import views as auth_views

from account.forms import CustomPasswordResetForm, CustomSetPasswordForm
from main.sitemaps import HomeViewSitemap, StaticViewSitemap

sitemaps = {
    'home': HomeViewSitemap,
    'static': StaticViewSitemap,
}

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path("", include('account.urls', namespace='account')),
    path("", include("main.urls", namespace="main")),
    path("", include('loan.urls', namespace='loan')),

    path("password-reset/", auth_views.PasswordResetView.as_view(template_name='auth/password-reset.html', html_email_template_name="auth/password-reset-email-template.html", form_class=CustomPasswordResetForm), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name='auth/password-reset-done.html'), name="password_reset_done"),
    path("password-reset/confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='auth/password-reset-confirm.html', form_class=CustomSetPasswordForm), name="password_reset_confirm"),
    path("password-reset/complete/", auth_views.PasswordResetCompleteView.as_view(template_name='auth/password-reset-complete.html'), name="password_reset_complete"),

    path("sitemap.xml/", sitemap, {'sitemaps': sitemaps}),
    path("robots.txt/", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),

    path('i18n/', include('django.conf.urls.i18n')),
)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [re_path(r'^rosetta/', include('rosetta.urls'))]

# Static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Error Pages
handler404 = 'main.views.not_found_view'
handler403 = 'main.views.forbidden_view'
handler500 = 'main.views.internal_server_error_view'

# handler404 = 'main.views.error_handler_view'
# handler403 = 'main.views.error_handler_view'
# handler500 = 'main.views.error_handler_view'
