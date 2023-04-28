import datetime
import json
import threading
import time

import requests

from asmcnc.comms.flurry.models.job import Job
from asmcnc.comms.flurry.models.machine import Machine
from asmcnc.comms.flurry.models.statistic import Statistic

WEB_API_URL = 'https://localhost:7109/api/'
VERIFY_SSL = False


def send_post_request(endpoint, data, url=WEB_API_URL):
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain', "Api-Key": "string"}
    r = requests.post(url + endpoint, data=json.dumps(data, default=vars), headers=headers, verify=VERIFY_SSL)

    if __name__ == "__main__":
        print(r.text)
        print(r.status_code)
    return r


class Flurry(object):

    current_job_id = None
    hostname = None

    def __init__(self, **kwargs):
        self.m = kwargs['machine']

    def send_alive(self):
        machine = Machine(
            hostname=self.hostname,
            last_seen=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        )

        data = machine.get_api_format()

        send_post_request(
            endpoint='alive',
            data=data)

    def send_job_start(self, job_name):
        job = Job(
            machine_hostname=self.hostname,
            name=job_name,
            start_time=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        )

        data = job.get_api_format()

        response = send_post_request(
                    endpoint='add_job_start',
                    data=data)

        if response.status_code == 200:
            self.current_job_id = response.text

    def send_update_job(self):
        job = Job(
            machine_hostname=self.hostname,
            id=self.current_job_id,
            percentage=50
        )

        data = job.get_api_format()

        send_post_request(
            endpoint='update_job',
            data=data)

    def send_add_statistic(self):
        statistic = Statistic(
            job_id=self.current_job_id,
            machine_hostname=self.hostname,
            time=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            digital_spindle_load=self.m.s.digital_spindle_ld_qdA,
        )

        data = statistic.get_api_format()

        send_post_request(
            endpoint='add_statistic',
            data=data)

    def send_statistic_stack(self):
        data = [statistic.get_api_format() for statistic in self.m.s.flurry_data_stack]

        for statistic in data:
            statistic['job_id'] = self.current_job_id

        send_post_request(
            endpoint='add_statistic_stack',
            data=data)

        self.m.s.flurry_data_stack[:] = []


# flurry = Flurry()
#
# flurry.current_job_id = 3
#
# flurry.send_add_statistic()

