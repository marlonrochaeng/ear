from random import randint


class JobMachine:
    def __init__(self, num_jobs):
        self.jobs = [dict()] * num_jobs

    def set_wt(self, job, machine, work):
        self.jobs[job][machine] = work

    def get_jm_value(self, job, machine):
        return self.jobs[job][machine]
