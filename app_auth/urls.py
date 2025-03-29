from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.auth_login, name="login"),
    path("forget-password/", views.forget_password, name="forget-password"),
    path(
        "reset-password/<str:auth_token>", views.reset_password, name="reset-password"
    ),
    path("logout/", views.auth_logout, name="logout"),
]
