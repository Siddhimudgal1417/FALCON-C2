from django.db import models


class Connections(models.Model):
    machine_id = models.CharField(max_length=10, primary_key=True)
    machine_name = models.TextField()
    machine_type = models.TextField()
    ip_address = models.TextField()
    listener_id = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)


class CommandHistory(models.Model):
    machine_id = models.CharField(max_length=10)
    command = models.TextField()
    output = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
