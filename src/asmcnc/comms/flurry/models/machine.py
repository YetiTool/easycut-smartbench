
class Machine:
    parameters = {}

    def __init__(self, hostname, last_seen=None, ip_address=None, software_version=None,
                 firmware_version=None, serial_number=None, model=None, name=None, location=None):
        self.parameters['hostname'] = hostname
        self.parameters['lastSeen'] = last_seen
        self.parameters['ipAddress'] = ip_address
        self.parameters['softwareVersion'] = software_version
        self.parameters['firmwareVersion'] = firmware_version
        self.parameters['serialNumber'] = serial_number
        self.parameters['model'] = model
        self.parameters['name'] = name
        self.parameters['location'] = location

    def get_api_format(self):
        return {
            str(key): self.parameters[key] for key in self.parameters if self.parameters[key] is not None
        }
