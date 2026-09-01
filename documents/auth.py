from collections.abc import Callable
from functools import wraps
from typing import Any

from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse


def get_current_user(request: HttpRequest):
    """Return the session-authenticated user or reject an anonymous request."""
    user = getattr(request, "user", AnonymousUser())
    if not user.is_authenticated:
        raise PermissionDenied("Authentication is required.")
    return user


def is_admin(request: HttpRequest):
    """Authorization dependency for all application admin routes."""
    user = get_current_user(request)
    if not user.is_staff:
        raise PermissionDenied("Administrator access is required.")
    return user


def admin_required(view: Callable[..., HttpResponse]) -> Callable[..., HttpResponse]:
    """Apply the is_admin dependency before an admin route runs."""
    @wraps(view)
    def wrapped(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        is_admin(request)
        return view(request, *args, **kwargs)
    return wrapped
