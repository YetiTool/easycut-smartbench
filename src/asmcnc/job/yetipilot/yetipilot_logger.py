class YetiPilotLogger(object):

    logs = []

    def add_log(self, spindle_load, job_time):
        self.logs.append({
            'spindle_load': spindle_load,
            'job_time': job_time
        })

    def get_logs(self):
        return self.logs