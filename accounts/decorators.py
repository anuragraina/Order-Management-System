from django.http import HttpResponse
from django.shortcuts import redirect


def not_authenticated(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return view_function(request, *args, **kwargs)

    return wrapper_function


def allow_access(user_types=[]):
    def decorator(view_function):
        def wrapper_function(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in user_types:
                return view_function(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorised!!!')

        return wrapper_function
    return decorator


def admin_access(view_function):
    def wrapper_function(request, *args, **kwargs):

        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'customer':
            return redirect('user-page')

        if group == 'admin':
            return view_function(request, *args, **kwargs)

    return wrapper_function

