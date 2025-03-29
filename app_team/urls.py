from django.urls import path
from . import views

urlpatterns = [
    path("listener/create/", views.create_listener, name="create-listener"),
    path(
        "listener/update/<str:listener_id>/",
        views.update_listener,
        name="update-listener",
    ),
    path(
        "listener/delete/<str:listener_id>/",
        views.delete_listener,
        name="delete-listener",
    ),
    path("command/add/", views.add_command, name="add-command"),
]
