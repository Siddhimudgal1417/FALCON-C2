from django.db import models


class Listeners(models.Model):
    listener_id = models.CharField(max_length=10, primary_key=True)
    listener_name = models.TextField()
    listener_type = models.TextField()
    listener_status = models.CharField(max_length=10)


class CommandPool(models.Model):
    machine_id = models.CharField(max_length=10)
    command = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
