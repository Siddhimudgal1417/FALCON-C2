from django.urls import path
from . import views

urlpatterns = [
    path("user/create/", views.create_user, name="create-user"),
    path("user/update/<str:username>/", views.update_user, name="update-user"),
    path("user/delete/<str:username>/", views.delete_user, name="delete-user"),
]
