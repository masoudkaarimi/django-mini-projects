from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func, redirect_url="/dashboard"):
    """
    Redirects authenticated users to 'redirect_url'; lets unauthenticated users access the view.
    """

    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(redirect_url)
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed=None, body="Access Denied"):
    """
    Restricts view access to users in 'allowed' groups; returns 'body' message for unauthorized users.
    """
    if allowed is None:
        allowed = []

    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse(body)

        return wrapper_func

    return decorator
