from django.shortcuts import render
from django.core.mail.message import EmailMultiAlternatives
from django.core.mail import BadHeaderError
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from falcon_c2.decorators import *
from falcon_c2.views import *
from .serializers import *
from .models import *
import secrets


@login_required(login_url="login")
@admin_only
def team_control(request):
    data = User.objects.all()
    return render(request, "app_admin/team_control.html", {"data": data})


@login_required(login_url="login")
@admin_only
def team_control(request):
    data = User.objects.all()
    return render(request, "app_admin/team_control.html", {"data": data})


@api_view(["POST"])
def create_user(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        username = serializer.validated_data.get("username")
        email = serializer.validated_data.get("email", "")

        user = User.objects.create(username=username)

        if send_auth_token(username, email):
            user.first_name = serializer.validated_data.get("first_name", "")
            user.last_name = serializer.validated_data.get("last_name", "")
            user.email = email
            user.set_password(generate_random_password())
            user.is_active = False

            group = Group.objects.get(name="team")
            user.groups.add(group)

            user.save()

            return Response(
                {
                    "status": "success",
                    "message": f"User created successfully. An email verification link has been sent to {user.email}",
                }
            )

    return Response(
        {
            "status": "error",
            "message": serializer.errors.values(),
        }
    )


@api_view(["POST"])
def update_user(request, username):
    user = User.objects.get(username=username)
    serializer = UserSerializer(instance=user, data=request.data)

    if serializer.is_valid():
        serializer.save()

        return Response({"status": "success", "message": "User updated successfully."})

    return Response(
        {
            "status": "error",
            "message": serializer.errors.values(),
        }
    )


@api_view(["DELETE"])
def delete_user(request, username):
    if User.objects.filter(username=username).delete():
        return Response({"status": "success", "message": "User deleted successfully."})

    return Response(
        {
            "status": "error",
            "message": "User deletion failed.",
        }
    )


def send_auth_token(username, email):
    auth_token = generate_auth_token()
    try:
        subject, from_email, to = (
            "Password Reset - Falcon C2",
            "FalconC2<support@falcon.c2>",
            email,
        )
        text_content = "Don't share this passoword with anyone"
        html_content = (
            "Hello " + username + ",<br/>"
            "Click the following link to reset your password: "
            "<a href='http://127.0.0.1:8000/auth/reset-password/"
            + auth_token
            + "'>Reset Password</a><br/>"
            "<p><strong>Important:</strong> This is a one-time access link.</p>"
        )
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        if msg.send():
            AuthTokens(username, auth_token).save()
            return True
    except BadHeaderError:
        return False


def generate_auth_token():
    while True:
        characters = string.ascii_letters + string.digits
        auth_token = "".join(random.choice(characters) for i in range(32))
        if not AuthTokens.objects.filter(auth_token=auth_token).exists():
            return auth_token


def generate_random_password():
    length = 16
    characters = string.ascii_letters + string.digits + string.punctuation
    password = "".join(secrets.choice(characters) for _ in range(length))
    return password
