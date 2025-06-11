from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.contrib.auth import views as auth_views
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import login, authenticate, logout, get_user_model, update_session_auth_hash

from core.utils import toast
from apps.account.models import Address
from apps.account.decorators import unauthenticated_user
from apps.account.tokens import account_activation_token
from apps.account.forms import RegisterForm, LoginForm, AddressForm, ProfileForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm

User = get_user_model()


class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'auth/password/password_reset.html'
    email_template_name = 'auth/password/password_reset_email.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('account:password_reset_done')

    @method_decorator(unauthenticated_user)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

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


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'auth/password/password_reset_done.html'

    @method_decorator(unauthenticated_user)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

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


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'auth/password/password_reset_confirm.html'
    form_class = SetPasswordForm
    success_url = reverse_lazy('account:password_reset_complete')

    @method_decorator(unauthenticated_user)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

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


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'auth/password/password_reset_complete.html'

    @method_decorator(unauthenticated_user)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

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


@unauthenticated_user
def register_view(request, *args, **kwargs):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # login(request, user)
            # return redirect("account:login")
            current_site = get_current_site(request)
            subject = _('Activate your Account')
            message = render_to_string('auth/registration/account_activation_email.html', {
                'user': user,
                'protocol': request.scheme,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            context = {
                "breadcrumb": [
                    {'title': _('Home'), 'url': reverse('shop:home')},
                    {'title': _('Register'), 'url': reverse('account:register')},
                    {'title': _('Email Confirmation'), 'url': None},
                ],
            }
            return render(request, 'auth/registration/account_register_email_confirm.html', context=context)

    form = RegisterForm()
    context = {
        "breadcrumb": [
            {'title': _('Home'), 'url': reverse('shop:home')},
            {'title': _('Register'), 'url': None},
        ],
        "heading": {
            "title": _("Create your account"),
            "subtitle": _("Please fill in your information to register."),
        },
        "form": form
    }
    return render(request, "auth/registration/account_register.html", context=context)


@unauthenticated_user
def account_activate_view(request, uidb64, token, *args, **kwargs):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        toast(request, _("Your account has been activated successfully! Welcome %(username)s to DigiShop.") % {'username': user.username}, level='success')
        return redirect('account:dashboard')

    context = {
        "breadcrumb": [
            {'title': _('Home'), 'url': reverse('shop:home')},
            {'title': _('Register'), 'url': reverse('account:register')},
            {'title': _('Invalid Activation'), 'url': None},
        ],
    }
    return render(request, 'auth/registration/account_activation_invalid.html', context=context)


@unauthenticated_user
def login_view(request, *args, **kwargs):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])

            if not user:
                toast(request, _("Username or Password is incorrect"), level='error')
                return redirect("account:login")

            if not user.is_active:
                toast(request, _("Your account is inactive. Please check your email for activation instructions."), level='error')
                return redirect("account:login")

            login(request, user)
            toast(request, _("Login successful! Welcome %(username)s to DigiShop.") % {'username': user.username}, level='success')
            return redirect("account:dashboard")

    form = LoginForm()
    context = {
        "breadcrumb": [
            {'title': _('Home'), 'url': reverse('shop:home')},
            {'title': _('Login'), 'url': None},
        ],
        "heading": {
            "title": _("Login to your account"),
            "subtitle": _("Please enter your credentials to access your account."),
        },
        "form": form
    }
    return render(request, "auth/login.html", context=context)


@login_required(login_url="account:login")
def logout_view(request, *args, **kwargs):
    logout(request)
    toast(request, _("Logout successful."), level="success")
    return redirect("shop:home")


@login_required(login_url="account:login")
def dashboard_view(request, *args, **kwargs):
    context = {
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
                'url': reverse('account:orders'),
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
                'url': reverse('account:payments'),
                'icon': 'payment'
            },
            {
                'title': _('Wallet'),
                'description': _('Manage your digital wallet'),
                'url': reverse('account:profile'),  # Todo: create this page
                'icon': 'wallet'
            },
            {
                'title': _('Reviews'),
                'description': _('Manage your product reviews'),
                'url': reverse('account:profile'),  # Todo: create this page
                'icon': 'reviews'
            },
            {
                'title': _('Wishlist'),
                'description': _('View your saved items'),
                'url': reverse('account:profile'),  # Todo: create this page
                'icon': 'wishlist'
            },
            {
                'title': _('Recently viewed'),
                'description': _('Browse your viewing history'),
                'url': reverse('account:profile'),  # Todo: create this page
                'icon': 'recently_viewed'
            }
        ]
    }

    return render(request, 'account/dashboard/index.html', context=context)


@login_required(login_url="account:login")
def profile_view(request, *args, **kwargs):
    profile_form = ProfileForm(instance=request.user)
    password_form = PasswordChangeForm(request.user)

    context = {
        "breadcrumb": [
            {'title': _('Home'), 'url': reverse('shop:home')},
            {'title': _('Account'), 'url': reverse('account:dashboard')},
            {'title': _('Personal Info'), 'url': None},
        ],
        "heading": {
            "title": _("Profile"),
            "subtitle": _("Manage your personal information and account settings."),
        },
        "profile_form": profile_form,
        "password_form": password_form,
    }

    return render(request, 'account/profile/profile.html', context=context)


@login_required(login_url="account:login")
def profile_update_view(request, *args, **kwargs):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user, partial=True)

        if form.is_valid():
            form.save()
            toast(request, _("Profile updated successfully."), level='success')
        else:
            error_msgs = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_msgs.append(f"{field}: {error}")
            toast(request, _("Please correct the errors below: ") + " ".join(error_msgs), level='error')

        return redirect('account:profile')

    form = ProfileForm(instance=request.user)
    context = {
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

    return render(request, 'account/profile/index.html', context=context)


@login_required(login_url="account:login")
def profile_update_avatar_view(request):
    if request.method == 'POST' and request.FILES.get('avatar'):
        profile = request.user.profile
        profile.avatar = request.FILES['avatar']
        profile.save()
        toast(request, _("Profile picture updated successfully."), level='success')

    return redirect(request.META.get('HTTP_REFERER', 'profile'))


@login_required(login_url="account:login")
def profile_update_password_view(request):
    if request.method == "POST":
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


@login_required(login_url="account:login")
def profile_delete_view(request, *args, **kwargs):
    if request.method == "POST":
        user = request.user
        permanent_delete = request.POST.get('permanent_delete', 'false').lower() == 'true'

        if user.delete_account(permanent=permanent_delete):
            logout(request)
            toast(request, _("Your account has been deleted successfully."), level='success')
            return redirect('shop:home')
        else:
            toast(request, _("There was a problem deleting your account. Please try again."), level='error')

    return redirect('account:profile')


@login_required(login_url="account:login")
def address_list_view(request, *args, **kwargs):
    addresses = Address.objects.filter(user=request.user).order_by('-is_default')

    context = {
        "breadcrumb": [
            {'title': _('Home'), 'url': reverse('shop:home')},
            {'title': _('Account'), 'url': reverse('account:dashboard')},
            {'title': _('Addresses'), 'url': None},
        ],
        "heading": {
            "title": _("Addresses"),
            "subtitle": _("Manage your addresses for shipping and billing."),
        },
        "addresses": addresses,
        "form": AddressForm(),
    }
    return render(request, 'account/address/address_list.html', context)


@login_required(login_url="account:login")
def address_detail_view(request, pk, *args, **kwargs):
    try:
        address = Address.objects.get(pk=pk, user=request.user)
    except Address.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': _("Address not found."),
        })

    form = AddressForm(instance=address)

    data = {}
    for field in form.fields:
        value = getattr(address, field)
        if hasattr(value, '__class__') and value.__class__.__name__ in ['PhoneNumber', 'Country']:
            data[field] = str(value)
        else:
            data[field] = value

    return JsonResponse({
        'success': True,
        'data': data
    })


@login_required(login_url="account:login")
def address_create_view(request, *args, **kwargs):
    if request.method == "POST":
        form = AddressForm(request.POST)

        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()

            return JsonResponse({
                'success': True,
                'message': _("Address added successfully."),
            })
        else:
            errors = {field: str(error[0]) for field, error in form.errors.items()}
            return JsonResponse({
                'success': False,
                'message': _("Failed to add address. Please check the form."),
                'errors': errors
            })
    return JsonResponse({
        'success': False,
        'message': _("Invalid request method. Use POST to add an address."),
    })


@login_required(login_url="account:login")
def address_update_view(request, pk, *args, **kwargs):
    if request.method == "POST":
        try:
            address = Address.objects.get(pk=pk, user=request.user)
        except Address.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': _("Address not found."),
            })

        form = AddressForm(request.POST, instance=address)

        if form.is_valid():
            form.save()

            return JsonResponse({
                'success': True,
                'message': _("Address updated successfully."),
            })
        else:
            errors = {field: str(error[0]) for field, error in form.errors.items()}
            return JsonResponse({
                'success': False,
                'message': _("Failed to update the address. Please check the form."),
                'errors': errors
            })
    return JsonResponse({
        'success': False,
        'message': _("Invalid request method. Use POST to update an address."),
    })


@login_required(login_url="account:login")
def address_delete_view(request, pk, *args, **kwargs):
    if request.method == "DELETE":
        try:
            address = Address.objects.get(pk=pk, user=request.user)
            address.delete()
            toast(request, _("Address deleted successfully."), level='success')
            return JsonResponse({
                'success': True,
                'message': _("Address deleted successfully."),
            })
        except Address.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': _("Address not found."),
            })
    return JsonResponse({
        'success': False,
        'message': _("Invalid request method. Use DELETE to remove an address."),
    })


@login_required(login_url="account:login")
def address_set_default_view(request, pk, *args, **kwargs):
    if request.method == "POST":
        try:
            address = Address.objects.get(pk=pk, user=request.user)
            address.is_default = True
            address.save()

            toast(request, _("Default address set successfully."), level='success')
            return JsonResponse({
                'success': True,
                'message': _("Default address set successfully."),
            })
        except Address.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': _("Address not found."),
            })

    return JsonResponse({
        'success': False,
        'message': _("Invalid request method. Use POST to set an address as default."),
    })


@login_required(login_url="account:login")
def orders_view(request, *args, **kwargs):
    context = {
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
    }

    return render(request, 'account/orders/index.html', context)


@login_required(login_url="account:login")
def order_detail_view(request, order_slug, *args, **kwargs):
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
    context = {
        "breadcrumb": [
            {'title': _('Home'), 'url': reverse('shop:home')},
            {'title': _('Account'), 'url': reverse('account:dashboard')},
            {'title': _('Orders'), 'url': reverse('account:order')},
            {'title': _('Order Details'), 'url': None},
        ],
        "heading": {
            "title": _("Order Details"),
            "subtitle": _("Order ID") + ": " + order["id"],
        },
        "order": order,
    }

    return render(request, 'account/orders/details.html', context)


@login_required(login_url="account:login")
def payments_view(request, *args, **kwargs):
    context = {
        "breadcrumb": [
            {'title': _('Home'), 'url': reverse('shop:home')},
            {'title': _('Account'), 'url': reverse('account:dashboard')},
            {'title': _('Payment Methods'), 'url': None},
        ],
        "heading": {
            "title": _("Payment Methods"),
            "subtitle": _("Manage your payment methods for easier checkout.")
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
    }

    return render(request, 'account/payments/index.html', context)
