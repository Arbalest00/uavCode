import simple_pid
class PID:
    def __init__(self,limit,target) -> None:
        self.p=1
        self.i=0.5
        self.d=0
        self.limit=limit
        self.pid=simple_pid.PID(self.p,self.i,self.d)
        self.pid.output_limits=(-self.limit,self.limit)
        pass
    def get_pid(self,current):
        return int(self.pid(current))
