class Statistic:

    parameters = {}

    def __init__(self, job_id, machine_hostname, time, digital_spindle_load):
        self.parameters['jobId'] = job_id
        self.parameters['machineHostname'] = machine_hostname
        self.parameters['time'] = time
        self.parameters['digitalSpindleLoad'] = digital_spindle_load

    def get_api_format(self):
        return {
            str(key): self.parameters[key] for key in self.parameters if self.parameters[key] is not None
        }