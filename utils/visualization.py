import time
import requests

TOKEN = "BBUS-0uskZVL6b5rQLpgl4JYU20HZYxNh03"
DEVICE_LABEL = "esp32-cam-uni268"
VARIABLE_LABEL_1 = "density_value"  
VARIABLE_LABEL_2 = "density_level"  
VARIABLE_LABEL_3 = "person_count"


def build_payload(variable_1: float, variable_2: str, variable_3: int):
    # Creates two random values for sending data
    
    payload = {
        "density_value": variable_1,
        "density_level": {
            "value": variable_2,
            "context": {
                "unit": "persons/m²"
            }
        },
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
