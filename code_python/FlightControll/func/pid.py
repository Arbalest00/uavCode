import simple_pid
class PID:
    #飞机使用 type0为xypid type1为yawpid
    def __init__(self,type=0,target=0) -> None:
        self.xyp=0.7
        self.xyi=0.002
        self.xyd=0.00
        self.yawp=1.5
        self.yawi=0.0
        self.yawd=0.3
        self.xylimit=40
        self.yawlimit=30 
        self.type=type
        self.target=target
    def pid_init(self):
        if self.type==0:
            self.pid=simple_pid.PID(self.xyp,self.xyi,self.xyd,self.target)
            self.pid.output_limits=(-self.xylimit,self.xylimit)
        else:
            self.pid=simple_pid.PID(self.yawp,self.yawi,self.yawd,self.target)
            self.pid.output_limits=(-self.yawlimit,self.yawlimit)
        pass
    def get_pid(self,current):
        return self.pid(current)
class PID2(PID):
    #车使用 目前废弃
    def __init__(self,type=0,target=0) -> None:
        self.xyp=0.25
        self.xyi=0.003
        self.xyd=0.007
        self.yawp=1.5
        self.yawi=0.0
        self.yawd=0.3
        self.xylimit=25
        self.yawlimit=30
        self.type=type
        self.target=target
    def get_pid(self,current):
        return int(self.pid(current))
class PID3(PID2):
    #我也忘了是哪里用的了
    def __init__(self,type=0,target=0) -> None:
        self.xylimit=20
        self.yawlimit=15
        self.type=type
        self.target=target
    def get_pid(self,current):
        return int(self.pid(current)*0.5)