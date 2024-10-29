from functools import wraps
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
#decorator untuk membatasi role apa saja yang boleh mengakses view
def role_required(allowed_roles=[]):
    def decorator(view_function):
        def wrapper(request, *args, **kwargs):
            if request.user.is_staff or request.user.role in allowed_roles:
                return  view_function(request, *args, **kwargs)
            else:
                return redirect('admin_setori:halaman_login')
                # raise PermissionDenied
        return wrapper
    return decorator

def admin_only():
    def decorator(view_function):
        def wrapper(request, *args, **kwargs):
            if request.user.is_staff:
                print('testttt')
                return  view_function(request, *args, **kwargs)
            else:
                return redirect('admin_setori:halaman_login')
        return wrapper
    return decorator
