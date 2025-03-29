from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from app_admin.models import AuthTokens
from app_admin.views import send_auth_token
from falcon_c2.decorators import *


@unauthenticated_user
def auth_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except Exception:
            return render(
                request,
                "app_auth/login.html",
                {"error": "Incorrect username or password."},
            )

        if not user.is_active:
            return render(
                request,
                "app_auth/login.html",
                {"error": "Please verify your email address to proceed."},
            )

        if user.check_password(password):
            request.session["is_admin"] = False
            login(request, user)
            if user.is_superuser:
                request.session["is_admin"] = True
                return redirect("team-control")
            return redirect("listeners")
        else:
            return render(
                request,
                "app_auth/login.html",
                {"error": "Incorrect username or password."},
            )

    return render(request, "app_auth/login.html")


@unauthenticated_user
def forget_password(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)
            if send_auth_token(user.username, user.email):
                return render(
                    request,
                    "app_auth/forget_password.html",
                    {"success": f"Password reset link has been sent to {user.email}"},
                )
            else:
                return render(
                    request,
                    "app_auth/forget_password.html",
                    {
                        "error": "Failed to send password reset email. Please try again later!."
                    },
                )
        except Exception:
            return render(
                request,
                "app_auth/forget_password.html",
                {"error": f"User with email {email} does not exist."},
            )

    return render(request, "app_auth/forget_password.html")


@unauthenticated_user
def reset_password(request, auth_token):
    try:
        username = AuthTokens.objects.get(auth_token=auth_token).username
    except Exception:
        return render(
            request,
            "app_auth/reset_password.html",
            {"error_invalid_token": "Invalid or expired verification link."},
        )

    if request.method == "POST":
        new_password = request.POST.get("password")
        new_confirm_password = request.POST.get("confirm_password")

        if new_password == new_confirm_password:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.is_active = True
            user.save()
            AuthTokens.objects.filter(auth_token=auth_token).delete()
            return render(
                request,
                "app_auth/reset_password.html",
                {"success": "Password updated successfully. Please login again!"},
            )
        else:
            return render(
                request,
                "app_auth/reset_password.html",
                {"username": username, "error": "Passwords doesn't match."},
            )

    return render(request, "app_auth/reset_password.html", {"username": username})


@login_required(login_url="login")
def auth_logout(request):
    logout(request)
    return redirect("login")
