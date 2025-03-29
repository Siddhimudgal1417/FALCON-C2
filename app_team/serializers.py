from rest_framework import serializers
from .models import *


class ListenersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listeners
        fields = "__all__"


class CommandPoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommandPool
        fields = "__all__"
