from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from falcon_c2.decorators import *
from falcon_c2.views import *
from c2_api.models import *
from c2_api.serializers import *
from .serializers import *
from .models import *


@login_required(login_url="login")
def listeners(request):
    data = Listeners.objects.all()
    return render(request, "app_team/listeners.html", {"data": data})


@login_required(login_url="login")
def connections(request, listener_id=None):
    if listener_id is not None:
        data = Connections.objects.filter(listener_id=listener_id)
    else:
        data = Connections.objects.all()
        listener_id = "All"

    return render(
        request,
        "app_team/connections.html",
        {"listener_id": listener_id, "data": data},
    )


@login_required(login_url="login")
def machines(request, machine_id=None):
    if machine_id is not None:
        data = CommandHistory.objects.filter(machine_id=machine_id).order_by('-timestamp')
    else:
        data = CommandHistory.objects.all().order_by('-timestamp')
        machine_id = "All"

    for d in data:
        d.output = decode_base64_string(d.output)

    return render(
        request,
        "app_team/machines.html",
        {"machine_id": machine_id, "data": data},
    )


@api_view(["POST"])
def create_listener(request):
    data = remove_csrf(request.data.copy())
    data["listener_id"] = generate_id(Listeners, "listener_id")

    serializer = ListenersSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "status": "success",
                "message": "Listener created successfully.",
            }
        )

    return Response(
        {
            "status": "error",
            "message": serializer.errors.values(),
        }
    )


@api_view(["POST"])
def update_listener(request, listener_id):
    listener = Listeners.objects.get(listener_id=listener_id)
    serializer = ListenersSerializer(instance=listener, data=request.data)

    if serializer.is_valid():
        serializer.save()

        return Response(
            {"status": "success", "message": "Listener updated successfully."}
        )

    return Response(
        {
            "status": "error",
            "message": serializer.errors.values(),
        }
    )


@api_view(["DELETE"])
def delete_listener(request, listener_id):
    if Listeners.objects.filter(listener_id=listener_id).delete():
        return Response(
            {"status": "success", "message": "Listener deleted successfully."}
        )

    return Response(
        {
            "status": "error",
            "message": "Listener deletion failed.",
        }
    )


@api_view(["POST"])
def add_command(request):
    data = remove_csrf(request.data.copy())
    serializer = CommandPoolSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "status": "success",
                "command": data.get("command"),
            }
        )

    return Response(
        {
            "status": "error",
            "message": serializer.errors.values(),
        }
    )
