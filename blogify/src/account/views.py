from django.shortcuts import render, redirect
from django.views import View
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.utils.decorators import method_decorator

from main.utils import toast
from account.forms import RegisterForm, CustomPasswordChangeForm, CustomUserChangeForm, LoginForm
from account.decorators import unauthenticated_user


class Auth(View):
    @classmethod
    @method_decorator(unauthenticated_user)
    def register_view(cls, request, *args, **kwargs):
        if request.method == "POST":
            form = RegisterForm(request.POST)

            if form.is_valid():
                user = form.save()
                login(request, user)
                toast(request, _("Welcome %(username)s.") % {'username': user.username}, level='success')
                return redirect("account:profile")
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

    @classmethod
    @method_decorator(unauthenticated_user)
    def login_view(cls, request, *args, **kwargs):
        if request.method == "POST":
            form = LoginForm(request.POST)

            if form.is_valid():
                user = authenticate(request, username=form.cleaned_data['identity'], password=form.cleaned_data['password'])

                if user:
                    login(request, user)
                    toast(request, _("Welcome %(username)s.") % {'username': user.username}, level='success')
                    return redirect("account:profile")
                else:
                    toast(request, _("Email or Password is incorrect."), level="error")
                    return redirect("account:login")
            else:
                toast(request, form.errors, level="error")

        old_data = {
            "identity": request.POST.get("identity", None),
            "password": request.POST.get("password", None),
        }
        form = LoginForm(initial=old_data)
        context = {"title": _("Login"), "form": form}
        return render(request, "auth/login.html", context)

    @classmethod
    @method_decorator(login_required(login_url="/login"))
    def logout_view(cls, request, *args, **kwargs):
        logout(request)
        toast(request, _("Logout successful."), level="success")
        return redirect("account:login")

    @classmethod
    @method_decorator(login_required(login_url="/login"))
    def password_change_view(cls, request, *args, **kwargs):
        if request.method == "POST":
            form = CustomPasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                toast(request, _(f"Your password was successfully updated."), level="success")
                return redirect("account:profile")
            else:
                toast(request, form.errors, level="error")
                return redirect("account:profile")

        # Todo: Create a password change template
        # form = CustomPasswordChangeForm(request.user)
        # return render(request, "auth/password-change-template.html", {'form': form})

    @classmethod
    @method_decorator(login_required(login_url="/login"))
    def profile_view(cls, request, *args, **kwargs):
        user = request.user

        if request.method == "POST":
            form = CustomUserChangeForm(instance=user, data=request.POST)

            if form.is_valid():
                form.save()
                toast(request, _(f"%(username)s's profile was updated successfully.") % {'username': user.username}, level="success")
                return redirect("account:profile")
            else:
                toast(request, form.errors, level="error")
                return redirect("account:profile")

        form = CustomUserChangeForm(instance=user)
        context = {"title": _(f"%(username)s's profile") % {'username': user.username}, "form": form}
        return render(request, "dashboard/profile.html", context)
