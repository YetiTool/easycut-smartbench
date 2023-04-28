class Job:

    parameters = {}

    def __init__(self, machine_hostname, id=None, name=None, start_time=None, end_time=None, time_elapsed=None,
                 percentage=None, gcode_line=None, gcode=None):
        self.parameters['machineHostname'] = machine_hostname
        self.parameters['id'] = id
        self.parameters['name'] = name
        self.parameters['startTime'] = start_time
        self.parameters['endTime'] = end_time
        self.parameters['timeElapsed'] = time_elapsed
        self.parameters['percentage'] = percentage
        self.parameters['gcodeLine'] = gcode_line
        self.parameters['gcode'] = gcode

    def get_api_format(self):
        return {
            str(key): self.parameters[key] for key in self.parameters if self.parameters[key] is not None
        }