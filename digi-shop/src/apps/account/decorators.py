import functools
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from django.urls import reverse


def unauthenticated_user(view_func=None, redirect_url=None):
    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                url = redirect_url or 'account:dashboard'
                redirect_path = reverse(url) if ':' in url else url
                return redirect(redirect_path)
            return view_func(request, *args, **kwargs)

        return wrapper

    if view_func is None:
        return decorator
    return decorator(view_func)


def allowed_users(allowed_roles=None):
    allowed_roles = allowed_roles or []

    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Authentication required")

            # Allow superusers to bypass restrictions
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            # Check if user belongs to any of the allowed groups
            user_groups = request.user.groups.values_list('name', flat=True)
            if any(role in user_groups for role in allowed_roles):
                return view_func(request, *args, **kwargs)

            return HttpResponseForbidden("You don't have permission to access this page")

        return wrapper

    return decorator


def staff_required(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account:login')

        if request.user.is_staff:
            return view_func(request, *args, **kwargs)

        return HttpResponseForbidden("Staff access required")

    return wrapper
