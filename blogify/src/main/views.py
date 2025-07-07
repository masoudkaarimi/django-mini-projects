from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views import View
from django.utils.translation import gettext as _

from main.utils import toast
from main.forms import ContactForm


class MainView(View):
    @classmethod
    def home_view(cls, request, *args, **kwargs):
        context = {'title': _("Home")}
        return render(request, "main/home.html", context)

    @classmethod
    def about_view(cls, request, *args, **kwargs):
        context = {'title': _("About Us")}
        return render(request, "main/about.html", context)

    @classmethod
    def contact_view(cls, request, *args, **kwargs):
        if request.method == "POST":
            form = ContactForm(request.POST)

            if form.is_valid():
                name = form.cleaned_data.get("name")
                subject = form.cleaned_data.get("subject")
                email = form.cleaned_data.get("email")
                message = form.cleaned_data.get("message")

                recipient = ["info@example.com"]
                send_mail(subject, f"Name: {name}\nEmail: {email}\n\n{message}", email, recipient, fail_silently=True)
                toast(request, _("Your message has been sent successfully."), level="success")
                return redirect('main:contact')
            else:
                toast(request, form.errors, level="error")

        old_data = {
            "name": request.POST.get("name", None),
            "subject": request.POST.get("subject", None),
            "email": request.POST.get("email", None),
            "message": request.POST.get("message", None),
        }
        form = ContactForm(initial=old_data)
        context = {'title': _("Contact Us"), 'form': form}
        return render(request, "main/contact.html", context)

    @classmethod
    def privacy_view(cls, request, *args, **kwargs):
        context = {'title': _("Privacy Policy")}
        return render(request, "main/privacy.html", context)
