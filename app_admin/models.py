from django.db import models


class AuthTokens(models.Model):
    username = models.CharField(max_length=25, primary_key=True)
    auth_token = models.CharField(max_length=32)
