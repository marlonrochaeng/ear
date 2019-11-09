from random import randint

class Job:
    def __init__(self):
        self.work_time = randint(1,100)

    def __str__(self):
            return("work_time: "+str(self.work_time))
    
    def __repr__(self):
        return str(self)