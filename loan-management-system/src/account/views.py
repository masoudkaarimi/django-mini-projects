from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash

from core.utils import toast
from account.decorators import unauthenticated_user
from account.forms import StylesCustomUserChangeForm, CustomPasswordChangeForm, RegisterForm


@unauthenticated_user
def register_view(request, *args, **kwargs):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user, backend="account.backends.EmailBackend")
            toast(request, _(f"Welcome {user.username}."), level='success')
            return redirect("loan:dashboard")
        else:
            toast(request, form.errors, level="error")

    old_data = {
        "first_name": request.POST.get("first_name", None),
        "last_name": request.POST.get("last_name", None),
        "username": request.POST.get("username", None),
        "email": request.POST.get("email", None),
        "phone": request.POST.get("phone", None),
    }
    form = RegisterForm(initial=old_data)
    context = {"title": _("Register"), "form": form}

    return render(request, "auth/register.html", context)


@unauthenticated_user
def login_view(request, *args, **kwargs):
    if request.method == "POST":
        email = request.POST.get("email", None)
        password = request.POST.get("password", None)

        if not email or not password:
            error_message = _("Email is required.") if not email else _("Password is required.")
            toast(request, error_message, level="error")
            return redirect(request.META.get("HTTP_REFERER", "account:login"))

        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user, backend="account.backends.EmailBackend")
            toast(request, _(f"Welcome {user.username}."), level='success')
            return redirect("loan:dashboard")
        else:
            toast(request, _("Email or Password is incorrect."), level="error")
            return redirect(request.META.get("HTTP_REFERER", "account:login"))

    context = {"title": _("Login")}
    return render(request, "auth/login.html", context)


@login_required(login_url="/login")
def logout_view(request, *args, **kwargs):
    logout(request)
    toast(request, _("Logout successful."), level="success")
    return redirect("account:login")


@login_required(login_url="/login")
def password_change_view(request, *args, **kwargs):
    if request.method == "POST":
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            toast(request, _(f"Your password was successfully updated."), level="success")
            return redirect("account:profile")
        else:
            toast(request, form.errors, level="error")
            return redirect(request.META.get("HTTP_REFERER", "account:profile"))

    # TODO: Create a password change template
    # form = CustomPasswordChangeForm(request.user)
    # return render(request, "path/to/password_change_template.html", {'form': form})
    raise Http404("Page not found")


@login_required(login_url="/login")
def profile_view(request, *args, **kwargs):
    user = request.user

    if request.method == "POST":
        form = StylesCustomUserChangeForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            toast(request, _(f"Profile updated successfully"), level="success")
            return redirect("account:profile")
        else:
            toast(request, form.errors, level="error")
            return redirect(request.META.get("HTTP_REFERER", "account:profile"))

    form = StylesCustomUserChangeForm(instance=user)
    password_form = CustomPasswordChangeForm(user)
    context = {"title": _(f"Profile | {request.user}"), "form": form, "password_form": password_form}
    return render(request, "dashboard/profile.html", context)
