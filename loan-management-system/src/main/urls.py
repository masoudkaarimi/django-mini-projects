from django.urls import path

from .views import home_view, about_view, contact_view, privacy_view

app_name = "main"

urlpatterns = [
    path("", home_view, name="home"),
    path("about/", about_view, name="about"),
    path("contact/", contact_view, name="contact"),
    path("privacy/", privacy_view, name="privacy"),
]
