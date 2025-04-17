import requests
from time import sleep

TOKEN = "BBUS-0uskZVL6b5rQLpgl4JYU20HZYxNh03"
DEVICE_LABEL = "esp32-cam-uni268"
VARIABLE_LABEL_1 = "density_value"  
VARIABLE_LABEL_2 = "density_level"  
VARIABLE_LABEL_3 = "person_count"


def build_payload(variable_1: float, variable_2: str, variable_3: int):
    payload = {
        "density_value": variable_1,
        "density_level": variable_2,
        "person_count": variable_3
    }

    return payload


def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        sleep(1)

    # Processes results
    print("")
    print(req.status_code, req.json())
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False
    
    sleep(5)
    print("[INFO] request made properly, your device is updated")
    return True