from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                if group == "team":
                    return redirect("listeners")
                elif group == "admin":
                    return redirect("team-control")
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            if group == "team":
                return redirect("listeners")
            if group == "admin":
                return view_func(request, *args, **kwargs)

    return wrapper_function
