import json
import threading
import requests


class MachineStatus:
    def __init__(self, mX, mY, mZ, digital_spindle_load_qda, timestamp):
        self.mX = mX
        self.mY = mY
        self.mZ = mZ
        self.digital_spindle_load_qda = digital_spindle_load_qda
        self.timestamp = timestamp


WEB_API_URL = 'https://localhost:7109/api/'
WEB_API_URL = 'https://beta.sm.yetitool.com/api/'

# IMPORTANT
VERIFY_SSL = True


def send_post_request(endpoint, data, url=WEB_API_URL):
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain', "Api-Key": "string"}
    r = requests.post(url + endpoint, data=json.dumps(data, default=vars), headers=headers, verify=VERIFY_SSL)
    print(r.text)
    print(r.status_code)


class Flurry:
    def __init__(self, **kwargs):
        pass

    """
    Update Machine Status
    """
    _update_machine_status_queue = []
    _update_machine_status_max = 1

    def _update_machine_status(self):
        send_post_request(
            endpoint='update_machine_status',
            data=self._update_machine_status_queue)
        self._update_machine_status_queue = []

    def update_machine_status(self, machine_status):
        self._update_machine_status_queue.append(machine_status)

        if self._update_machine_status_max == len(self._update_machine_status_queue):
            threading.Thread(target=self._update_machine_status).start()


# from datetime import datetime
# from random import randint
#
# flurry = Flurry()
#
# for i in range(50):
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     machine_status = MachineStatus(mX=randint(1, 10), mY=2, mZ=3, digital_spindle_load_qda=i, timestamp=timestamp)
#     flurry.update_machine_status(machine_status)