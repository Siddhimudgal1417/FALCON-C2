from django.shortcuts import redirect
import random
import string
import base64

def index(request):
    return redirect("login")


def generate_id(Model, id_field):
    id_length = 10
    while True:
        id = "".join(random.choice(string.hexdigits.lower()) for _ in range(id_length))
        if not Model.objects.filter(**{f"{id_field}__exact": id}).exists():
            return id


def remove_csrf(data):
    if "csrfmiddlewaretoken" in data:
        del data["csrfmiddlewaretoken"]
    return data

def decode_base64_string(encoded_string):
    decoded_bytes = base64.b64decode(encoded_string)
    return decoded_bytes.decode("utf-8")
