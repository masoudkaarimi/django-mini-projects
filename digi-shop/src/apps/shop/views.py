from django.db.models import Count
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext as _
from django.views.generic import TemplateView, FormView

from apps.common.utils import toast
from apps.shop.forms import ContactForm
from apps.shop.models import SliderBanner, FAQ
from apps.inventory.models import Product, Category


class HomeView(TemplateView):
    template_name = 'shop/home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slider_banners = SliderBanner.objects.filter(is_active=True).order_by('order')[:2]
        categories = (Category.objects.annotate(product_count=Count('products')).order_by('-product_count')[:6])
        featured_products = Product.objects.filter(is_featured=True, is_active=True).order_by('-created_at')[:4]
        context.update({
            "slider_banners": slider_banners,
            "categories": categories,
            "featured_products": featured_products,
        })

        return context


class ContactView(FormView):
    form_class = ContactForm
    template_name = "shop/contact/contact.html"
    success_url = reverse_lazy('shop:contact')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "breadcrumb": [
                {'title': _('Home'), 'url': reverse('shop:home')},
                {'title': _('Contact'), 'url': None},
            ],
            "heading": {
                "title": _("Contact Us"),
                "subtitle": _("We'd love to hear from you. Please fill out the form below."),
            },
        })
        return context

    def form_valid(self, form):
        name = form.cleaned_data.get("name")
        subject = form.cleaned_data.get("subject")
        email = form.cleaned_data.get("email")
        message = form.cleaned_data.get("message")

        recipient = ["info@example.com"]
        send_mail(subject, f"Name: {name}\nEmail: {email}\n\n{message}", email, recipient, fail_silently=True)
        toast(self.request, _("Your message has been sent successfully."), level="success")
        return super().form_valid(form)

    def form_invalid(self, form):
        toast(self.request, form.errors, level="error")
        return super().form_invalid(form)


class AboutView(TemplateView):
    template_name = 'shop/about/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "breadcrumb": [
                {'title': _('Home'), 'url': reverse('shop:home')},
                {'title': _('About'), 'url': None},
            ],
            "heading": {
                "title": _("About Us"),
                "subtitle": _("Learn more about our mission, vision, and values."),
            },
        })
        return context


class FAQView(TemplateView):
    template_name = 'shop/faq/faq.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        faqs = FAQ.objects.filter(is_active=True).order_by('order')

        context.update({
            "breadcrumb": [
                {'title': _('Home'), 'url': reverse('shop:home')},
                {'title': _('FAQ'), 'url': None},
            ],
            "heading": {
                "title": _("Frequently Asked Questions"),
                "subtitle": _("Find answers to common questions about our products and services."),
            },
            "faqs": faqs,
        })
        return context


class TermsView(TemplateView):
    template_name = 'shop/terms/terms.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "breadcrumb": [
                {'title': _('Home'), 'url': reverse('shop:home')},
                {'title': _('Terms and Conditions'), 'url': None},
            ],
            "heading": {
                "title": _("Terms and Conditions"),
                "subtitle": _("Read our terms and conditions before using our services."),
            },
        })
        return context


class NotFoundView(TemplateView):
    template_name = '404.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "breadcrumb": [
                {'title': _('Home'), 'url': reverse('shop:home')},
                {'title': _('404'), 'url': None},
            ],
            "heading": {
                "title": _("404: Page Not Found"),
                "subtitle": _("The page you are looking for does not exist or has been moved."),
            },
        })
        return context


class ForbiddenView(TemplateView):
    template_name = '403.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "breadcrumb": [
                {'title': _('Home'), 'url': reverse('shop:home')},
                {'title': _('403'), 'url': None},
            ],
            "heading": {
                "title": _("403: Forbidden"),
                "subtitle": _("You don't have permission to access this page."),
            },
        })
        return context


class InternalServerErrorView(TemplateView):
    template_name = '500.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "breadcrumb": [
                {'title': _('Home'), 'url': reverse('shop:home')},
                {'title': _('500'), 'url': None},
            ],
            "heading": {
                "title": _("500: Internal Server Error"),
                "subtitle": _("Something went wrong on our end. Please try again later."),
            },
        })
        return context
