from rest_framework import serializers
from .models import *


class ConnectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connections
        fields = "__all__"

class CommandHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommandHistory
        fields = "__all__"
