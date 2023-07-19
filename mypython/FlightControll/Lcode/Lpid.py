import simple_pid
class PID:
    def __init__(self,type=0,target=0) -> None:
        self.xyp=0.5
        self.xyi=0.003
        self.xyd=0.012
        self.yawp=2.5
        self.yawi=0.3
        self.yawd=0.02
        self.xylimit=50
        self.yawlimit=30
        if type==0:
            self.pid=simple_pid.PID(self.xyp,self.xyi,self.xyd,target)
            self.pid.output_limits=(-self.xylimit,self.xylimit)
        else:
            self.pid=simple_pid.PID(self.yawp,self.yawi,self.yawd,target)
            self.pid.output_limits=(-self.yawlimit,self.yawlimit)
        pass
    def get_pid(self,current):
        return int(self.pid(current))
