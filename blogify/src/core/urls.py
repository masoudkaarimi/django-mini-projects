from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include, re_path
from django.views.generic import TemplateView

from main.sitemaps import HomeViewSitemap, StaticViewSitemap
from account.forms import CustomPasswordResetForm, CustomSetPasswordForm

sitemaps = {
    'home': HomeViewSitemap,
    'static': StaticViewSitemap,
}

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),

    path("password-reset/", auth_views.PasswordResetView.as_view(template_name='auth/password-reset.html', html_email_template_name="auth/password-reset-email-template.html", form_class=CustomPasswordResetForm), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name='auth/password-reset-done.html'), name="password_reset_done"),
    path("password-reset/confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='auth/password-reset-confirm.html', form_class=CustomSetPasswordForm), name="password_reset_confirm"),
    path("password-reset/complete/", auth_views.PasswordResetCompleteView.as_view(template_name='auth/password-reset-complete.html'), name="password_reset_complete"),

    path("sitemap.xml/", sitemap, {'sitemaps': sitemaps}),
    path("robots.txt/", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),

    path('i18n/', include('django.conf.urls.i18n')),
    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),

    path("", include('account.urls', namespace='account')),
    path("", include("main.urls", namespace="main")),
    path("", include('blog.urls', namespace='blog')),
)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [re_path(r'^rosetta/', include('rosetta.urls'))]

# Static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
