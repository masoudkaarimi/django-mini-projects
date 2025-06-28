from django.views import View
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext as _
from django.template.loader import render_to_string
from django.contrib.auth import views as auth_views
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, FormView, TemplateView
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import login, authenticate, logout, get_user_model, update_session_auth_hash

from apps.common.mixins import AnonymousRequiredMixin
from apps.common.utils import toast
from apps.account.models import Address, Wishlist
from apps.account.tokens import account_activation_token
from apps.account.forms import RegisterForm, LoginForm, AddressForm, ProfileForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm

User = get_user_model()


class RegisterView(AnonymousRequiredMixin, FormView):
    form_class = RegisterForm
    template_name = "auth/registration/register.html"
    success_url = reverse_lazy('account:register')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        current_site = get_current_site(self.request)
        subject = _('Activate your Account')
        message = render_to_string('auth/registration/activation_email.html', {
            'user': user,
            'protocol': self.request.scheme,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        user.email_user(subject=subject, message=message)

        return render(self.request, 'auth/registration/activation_email_sent.html', context={
            "breadcrumb": [
                {'title': _('Home'), 'url': reverse('shop:home')},
                {'title': _('Register'), 'url': reverse('account:register')},
                {'title': _('Email Confirmation'), 'url': None},
            ],
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "breadcrumb": [
                {'title': _('Home'), 'url': reverse('shop:home')},
                {'title': _('Register'), 'url': None},
            ],
            "heading": {
                "title": _("Create your account"),
                "subtitle": _("Please fill in your information to register."),
            },
        })

        return context


class AccountActivateView(AnonymousRequiredMixin, View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            if not user.is_active:
                user.is_active = True
                user.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                toast(request, _("Your account has been activated successfully! Welcome %(username)s to DigiShop.") % {'username': user.username}, level='success')
            else:
                toast(request, _("Your account is already active."), level='info')
            return redirect('account:dashboard')

        context = {
            "breadcrumb": [
                {'title': _('Home'), 'url': reverse('shop:home')},
                {'title': _('Register'), 'url': reverse('account:register')},
                {'title': _('Invalid Activation'), 'url': None},
            ],
        }

        return render(request, 'auth/registration/activation_invalid.html', context=context)


class LoginView(AnonymousRequiredMixin, FormView):
    form_class = LoginForm
    template_name = "auth/login.html"
    success_url = reverse_lazy('account:dashboard')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)

        if not user:
            toast(self.request, _("Username or Password is incorrect"), level='error')
            return redirect('account:login')

        if not user.is_active:
            toast(self.request, _("Your account is inactive. Please check your email for activation instructions."), level='error')
            return redirect('account:login')

        login(self.request, user)
        toast(self.request, _("Login successful! Welcome %(username)s to DigiShop.") % {'username': user.username}, level='success')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "breadcrumb": [
                {'title': _('Home'), 'url': reverse_lazy('shop:home')},
                {'title': _('Login'), 'url': None},
            ],
            "heading": {
                "title": _("Login to your account"),
                "subtitle": _("Please enter your credentials to access your account."),
            },
        })
        return context


class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        toast(request, _("Logout successful."), level="success")
        return redirect('shop:home')


class PasswordResetView(AnonymousRequiredMixin, auth_views.PasswordResetView):
    template_name = 'auth/password/password_reset.html'
    email_template_name = 'auth/password/password_reset_email.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('account:password_reset_done')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "breadcrumb": [
                {'title': _('Home'), 'url': reverse('shop:home')},
                {'title': _("Reset Password"), 'url': None},
            ],
            "heading": {
                "title": _("Reset Password"),
                "subtitle": _("Enter your email address to receive a link to reset your password."),
            }
        })
        return context


class PasswordResetDoneView(AnonymousRequiredMixin, auth_views.PasswordResetDoneView):
    template_name = 'auth/password/password_reset_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "breadcrumb": [
                {'title': _('Home'), 'url': reverse('shop:home')},
                {'title': _("Password Reset Email Sent"), 'url': None},
            ],
            "heading": {
                "title": _("Password Reset Email Sent"),
                "subtitle": _("A link to reset your password has been sent to your email address. Please check your inbox."),
            }
        })
        return context


class PasswordResetConfirmView(AnonymousRequiredMixin, auth_views.PasswordResetConfirmView):
    template_name = 'auth/password/password_reset_confirm.html'
    form_class = SetPasswordForm
    success_url = reverse_lazy('account:password_reset_complete')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = _("Invalid Password Reset Link") if not context.get('validlink', False) else _("Reset Your Password")
        context.update({
            "breadcrumb": [
                {'title': _('Home'), 'url': reverse('shop:home')},
                {'title': title, 'url': None},
            ],
            "heading": {
                "title": title,
                "subtitle": _("Enter your new password below."),
            }
        })
        return context


class PasswordResetCompleteView(AnonymousRequiredMixin, auth_views.PasswordResetCompleteView):
    template_name = 'auth/password/password_reset_complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "breadcrumb": [
                {'title': _('Home'), 'url': reverse('shop:home')},
                {'title': _("Password Reset Complete"), 'url': None},
            ],
            "heading": {
                "title": _("Password Reset Complete"),
                "subtitle": _("Your password has been reset successfully. You can now log in with your new password."),
            }
        })
        return context


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "account/dashboard/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "breadcrumb": [
                {'title': _('Home'), 'url': reverse('shop:home')},
                {'title': _('Account'), 'url': None},
            ],
            "heading": {
                "title": _("My Account"),
                "subtitle": _("Manage your account settings and personal information."),
            },
            "dashboard_items": [
                {
                    'title': _('Personal Info'),
                    'description': _('Update your details, email preferences or password'),
                    'url': reverse('account:profile'),
                    'icon': 'personal_info'
                },
                {
                    'title': _('My Orders'),
                    'description': _('Check the status of your orders or see past orders'),
                    'url': reverse('account:order_list'),
                    'icon': 'orders'
                },
                {
                    'title': _('Addresses'),
                    'description': _('Manage your billing & shipping addresses'),
                    'url': reverse('account:address_list'),
                    'icon': 'addresses'
                },
                {
                    'title': _('Payment'),
                    'description': _('Manage credit cards'),
                    'url': reverse('account:payment_list'),
                    'icon': 'payment'
                },
                {
                    'title': _('Wallet'),
                    'description': _('Manage your digital wallet'),
                    'url': reverse('account:profile'),  # TODO: create this page
                    'icon': 'wallet'
                },
                {
                    'title': _('Reviews'),
                    'description': _('Manage your product reviews'),
                    'url': reverse('account:profile'),  # TODO: create this page
                    'icon': 'reviews'
                },
                {
                    'title': _('Wishlist'),
                    'description': _('View your saved items'),
                    'url': reverse('account:profile'),  # TODO: create this page
                    'icon': 'wishlist'
                },
                {
                    'title': _('Recently viewed'),
                    'description': _('Browse your viewing history'),
                    'url': reverse('account:profile'),  # TODO: create this page
                    'icon': 'recently_viewed'
                }
            ]
        })
        return context


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "account/profile/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "breadcrumb": [
                {'title': _('Home'), 'url': reverse('shop:home')},
                {'title': _('Account'), 'url': reverse('account:dashboard')},
                {'title': _('Personal Info'), 'url': None},
            ],
            "heading": {
                "title": _("Profile"),
                "subtitle": _("Manage your personal information and account settings."),
            },
            "profile_form": ProfileForm(instance=self.request.user.profile),
            "password_form": PasswordChangeForm(self.request.user),
        })
        return context


class ProfileUpdateView(LoginRequiredMixin, View):
    template_name = 'account/profile/profile.html'

    def get_context(self, form):
        return {
            "breadcrumb": [
                {'title': _('Home'), 'url': reverse('shop:home')},
                {'title': _('Account'), 'url': reverse('account:dashboard')},
                {'title': _('Personal Info'), 'url': None},
            ],
            "heading": {
                "title": _("Profile"),
                "subtitle": _("Manage your personal information and account settings."),
            },
            "form": form,
        }

    def get(self, request, *args, **kwargs):
        form = ProfileForm(instance=request.user.profile)
        return render(request, self.template_name, context=self.get_context(form))

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            toast(request, _("Profile updated successfully."), level='success')

            return redirect('account:profile')
        else:
            error_msgs = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_msgs.append(f"{field}: {error}")
            toast(request, _("Please correct the errors below: ") + " ".join(error_msgs), level='error')

            return render(request, self.template_name, context=self.get_context(form))


class ProfileAvatarUpdateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if 'avatar' in request.FILES:
            profile = request.user.profile
            profile.avatar = request.FILES['avatar']
            profile.save()
            toast(request, _("Profile picture updated successfully."), level='success')
        else:
            toast(request, _("No avatar image uploaded."), level='error')

        return redirect(request.META.get('HTTP_REFERER', reverse('account:profile')))


class ProfileUpdatePasswordView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            toast(request, _("Your password was successfully updated."), level='success')
            return redirect('account:profile')
        else:
            error_msgs = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_msgs.append(f"{field}: {error}")
            toast(request, _("Please correct the errors below: ") + " ".join(error_msgs), level='error')
            return redirect('account:profile')


class ProfileDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user
        permanent_delete = request.POST.get('permanent_delete', 'false').lower() == 'true'

        if user.delete_account(permanent=permanent_delete):
            logout(request)
            toast(request, _("Your account has been deleted successfully."), level='success')
            return redirect('shop:home')
        else:
            toast(request, _("There was a problem deleting your account. Please try again."), level='error')

        return redirect('account:profile')


class WishlistView(LoginRequiredMixin, ListView):
    template_name = 'account/wishlist/wishlist.html'
    context_object_name = 'products'

    def get_queryset(self):
        wishlist = get_object_or_404(Wishlist, user=self.request.user)
        return wishlist.products.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            "breadcrumb": [
                {'title': _('Home'), 'url': reverse('shop:home')},
                {'title': _('Account'), 'url': reverse('account:dashboard')},
                {'title': _('Wishlist'), 'url': None},
            ],
            "heading": {
                "title": _("My Wishlist"),
                "subtitle": _("Items you've saved for later"),
            }
        })

        return context


class AddressListView(LoginRequiredMixin, TemplateView):
    template_name = 'account/address/address_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "breadcrumb": [
                {'title': _('Home'), 'url': reverse('shop:home')},
                {'title': _('Account'), 'url': reverse('account:dashboard')},
                {'title': _('Addresses'), 'url': None},
            ],
            "heading": {
                "title": _("Addresses"),
                "subtitle": _("Manage your addresses for shipping and billing."),
            },
            "addresses": Address.objects.filter(user=self.request.user).order_by('-is_default'),
            "form": AddressForm(),
        })
        return context


class AddressDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        try:
            address = Address.objects.get(pk=pk, user=request.user)
        except Address.DoesNotExist:
            return JsonResponse({'success': False, 'message': _("Address not found.")})

        form = AddressForm(instance=address)
        data = {}
        for field in form.fields:
            value = getattr(address, field)
            if hasattr(value, '__class__') and value.__class__.__name__ in ['PhoneNumber', 'Country']:
                data[field] = str(value)
            else:
                data[field] = value

        return JsonResponse({'success': True, 'data': data})


class AddressCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return JsonResponse({
                'success': True,
                'message': _("Address added successfully."),
            })
        errors = {field: str(error[0]) for field, error in form.errors.items()}
        return JsonResponse({
            'success': False,
            'message': _("Failed to add address. Please check the form."),
            'errors': errors
        })


class AddressUpdateView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        address = get_object_or_404(Address, pk=pk, user=request.user)
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'success': True,
                'message': _("Address updated successfully."),
            })
        errors = {field: str(error[0]) for field, error in form.errors.items()}
        return JsonResponse({
            'success': False,
            'message': _("Failed to update the address. Please check the form."),
            'errors': errors
        })


class AddressDeleteView(LoginRequiredMixin, View):
    def delete(self, request, pk, *args, **kwargs):
        try:
            address = Address.objects.get(pk=pk, user=request.user)
            address.delete()
            toast(request, _("Address deleted successfully."), level='success')
            return JsonResponse({'success': True, 'message': _("Address deleted successfully.")})
        except Address.DoesNotExist:
            return JsonResponse({'success': False, 'message': _("Address not found.")})


class AddressSetDefaultView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        try:
            address = Address.objects.get(pk=pk, user=request.user)
            address.is_default = True
            address.save()
            toast(request, _("Default address set successfully."), level='success')
            return JsonResponse({'success': True, 'message': _("Default address set successfully.")})
        except Address.DoesNotExist:
            return JsonResponse({'success': False, 'message': _("Address not found.")})


class OrderListView(LoginRequiredMixin, TemplateView):
    template_name = 'account/order/order_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "breadcrumb": [
                {'title': _('Home'), 'url': reverse('shop:home')},
                {'title': _('Account'), 'url': reverse('account:dashboard')},
                {'title': _('Orders'), 'url': None},
            ],
            "heading": {
                "title": _("Order History"),
                "subtitle": _("View your past orders and their details."),
            },
            "orders": [
                {
                    "order_id": "ORD123456",
                    "date": "2023-10-01",
                    "status": "Shipped",
                    "total": "1299.99",
                    "items": [
                        {
                            "name": "Samsung Galaxy S24 Ultra Smartphone",
                            "price": "1299.99",
                            "quantity": 1,
                            "image_url": "/static/assets/images/placeholder.svg",
                            "link": "/products/samsung-galaxy-s24-ultra-smartphone",
                        }
                    ]
                },
                {
                    "order_id": "ORD123457",
                    "date": "2023-10-05",
                    "status": "Delivered",
                    "total": "2399.98",
                    "items": [
                        {
                            "name": "Apple iPhone 15 Pro Max",
                            "price": "1199.99",
                            "quantity": 2,
                            "image_url": "/static/assets/images/placeholder.svg",
                            "link": "/products/apple-iphone-15-pro-max",
                        }
                    ]
                }
            ]
        })

        return context


class OrderDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'account/order/order_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = {
            "id": "ORD123456",
            "date": "2023-10-01",
            "status": "Shipped",
            "total": "1299.99",
            "items": [
                {
                    "name": "Samsung Galaxy S24 Ultra Smartphone",
                    "price": "1299.99",
                    "quantity": 1,
                    "image_url": "/static/assets/images/placeholder.svg",
                    "link": "/products/samsung-galaxy-s24-ultra-smartphone",
                }
            ],
            "shipping_address": {
                "name": "James Collins",
                "address": "123 Main Street, Apt 4B",
                "city": "New York",
                "state": "NY",
                "zip": "10001",
                "country": "United States"
            },
            "payment_method": {
                "card_name": "James Collins",
                "card_type": "Visa",
                "card_last4": "4242"
            }
        }
        context.update({
            "breadcrumb": [
                {'title': _('Home'), 'url': reverse('shop:home')},
                {'title': _('Account'), 'url': reverse('account:dashboard')},
                {'title': _('Orders'), 'url': reverse('account:order')},
                {'title': _('Order Detail # %(order_id)s') % {'order_id': order["id"]}, 'url': None},
            ],
            "heading": {
                "title": _("Order Details"),
                "subtitle": _('Order ID: %(order_id)s') % {'order_id': order["id"]},
            },
            "order": order,
        })
        return context


class PaymentMethodListView(LoginRequiredMixin, TemplateView):
    template_name = 'account/payment/payment_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            "breadcrumb": [
                {'title': _('Home'), 'url': reverse('shop:home')},
                {'title': _('Account'), 'url': reverse('account:dashboard')},
                {'title': _('Payment Methods'), 'url': None},
            ],
            "heading": {
                "title": _("Payment Methods"),
                "subtitle": _("Manage your payment methods for easier checkout."),
            },
            "payment_methods": [
                {
                    "name": "Visa",
                    "last4": "4242",
                    "expiry": "12/25",
                    "is_default": True,
                    "id": "pm_visa_01"
                },
                {
                    "name": "MasterCard",
                    "last4": "1234",
                    "expiry": "11/24",
                    "is_default": False,
                    "id": "pm_mastercard_02"
                }
            ]
        })

        return context
