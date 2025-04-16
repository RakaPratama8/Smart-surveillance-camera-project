import time
import requests
import math
import random

TOKEN = "BBUS-0uskZVL6b5rQLpgl4JYU20HZYxNh03"
DEVICE_LABEL = "esp32-cam-uni268"
VARIABLE_LABEL_1 = "density_value"  
VARIABLE_LABEL_2 = "density_level"  
VARIABLE_LABEL_3 = "person_count"


def build_payload(variable_1: float, variable_2: str, variable_3: int):
    # Creates two random values for sending data
    density_value = variable_1 # float
    density_level = variable_2 # str
    person_count = variable_3 # int
    
    payload = {
        variable_1: density_value,
        variable_2: density_level,
        variable_3: person_count
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
        time.sleep(1)

    # Processes results
    print(req.status_code, req.json())
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True


# def main():
#     payload = build_payload(
#         VARIABLE_LABEL_1, VARIABLE_LABEL_2, VARIABLE_LABEL_3
#     )

#     print("[INFO] Attemping to send data")
#     post_request(payload)
#     print("[INFO] finished")


# if __name__ == '__main__':
#     while (True):
#         main()
#         time.sleep(1)
