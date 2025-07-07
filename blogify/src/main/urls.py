from django.urls import path

from main.views import MainView

app_name = "main"

urlpatterns = [
    # path("", MainView.home_view, name="home"),
    path("about/", MainView.about_view, name="about"),
    path("contact/", MainView.contact_view, name="contact"),
    path("privacy/", MainView.privacy_view, name="privacy"),
]
