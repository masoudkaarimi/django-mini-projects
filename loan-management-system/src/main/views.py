from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _

from main.forms import ContactForm
from core.utils import toast


def home_view(request, *args, **kwargs):
    context = {'title': _("Home")}
    return render(request, "main/home.html", context)


def about_view(request, *args, **kwargs):
    context = {'title': _("About Us")}
    return render(request, "main/about.html", context)


def contact_view(request, *args, **kwargs):
    form = ContactForm()

    if request.method == "POST":
        form_data = {
            "name": request.POST.get("name"),
            "email": request.POST.get("email"),
            "subject": request.POST.get("subject"),
            "message": request.POST.get("message"),
        }
        form = ContactForm(data=form_data)

        if form.is_valid():
            name = form.cleaned_data.get("name")
            subject = form.cleaned_data.get("subject")
            email = form.cleaned_data.get("email")
            message = form.cleaned_data.get("message")

            recipient = ["info@example.com"]
            send_mail(subject, f"Name: {name}\nEmail: {email}\n\n{message}", email, recipient, fail_silently=True)
            toast(request, _("Your message has been sent successfully."), level="success")
            return redirect('main:contact')

    context = {'title': _("Contact Us"), 'form': form}
    return render(request, "main/contact.html", context)


def privacy_view(request, *args, **kwargs):
    context = {'title': _("Privacy Policy")}
    return render(request, "main/privacy.html", context)


def not_found_view(request, *args, **kwargs):
    context = {'title': _("404: Page Not Found")}
    return render(request, "404.html", context, status=404)


def forbidden_view(request, *args, **kwargs):
    context = {'title': _("403: Forbidden - Access Denied")}
    return render(request, "403.html", context, status=403)


def internal_server_error_view(request, *args, **kwargs):
    context = {'title': _("500: Internal Server Error")}
    return render(request, "500.html", context, status=500)

# def error_handler_view(request, exception=None, template_name="404.html", *args, **kwargs):
#     return TemplateView.as_view(template_name=template_name, *args, **kwargs)(request, exception=exception)
