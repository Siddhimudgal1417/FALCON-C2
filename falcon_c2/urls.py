from django.contrib import admin
from django.urls import path, include
from app_admin import views as admin_views
from app_team import views as team_views
from . import views

urlpatterns = [
    path("superuser/", admin.site.urls),
    path("", views.index, name="index"),
    path("auth/", include("app_auth.urls")),
    path("admin/team-control/", admin_views.team_control, name="team-control"),
    path("admin/api/", include("app_admin.urls")),
    path("team/listeners/", team_views.listeners, name="listeners"),
    path("team/connections/", team_views.connections, name="connections-all"),
    path(
        "team/connections/<str:listener_id>/",
        team_views.connections,
        name="connections-listener",
    ),
    path("team/machines/", team_views.machines, name="machines-all"),
    path("team/machines/<str:machine_id>/", team_views.machines, name="machines-machine-id"),
    path("team/api/", include("app_team.urls")),
    path("c2_api/", include("c2_api.urls")),
]
