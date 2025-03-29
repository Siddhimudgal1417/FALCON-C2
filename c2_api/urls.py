from django.urls import path
from . import views

urlpatterns = [
    path("connection/create/", views.create_connection, name="create-connection"),
    path(
        "connection/update/<str:machine_id>/",
        views.update_connection,
        name="update-connection",
    ),
    path(
        "connection/manage/<str:machine_id>/",
        views.manage_connection,
        name="manage-connection",
    ),
]
