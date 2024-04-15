#!/usr/bin/python3
import robot_interface as sdk # type: ignore
from timer import Timer

HIGHLEVEL = 0xee

class Go1():
    def __init__(self):
        self.udp = sdk.UDP(HIGHLEVEL, 8080, "192.168.123.161", 8082)
        self.cmd = sdk.HighCmd()
        self.state = sdk.HighState()
        self.action = lambda: self.stop_cmd()
        self.start()

    def start(self):
        self.udp.InitCmdData(self.cmd)
        self.timer = Timer(callback=lambda: self.send_cmd(self.action))
        self.timer.start()        

    def reset_cmd(self):
        self.cmd.mode = 0      
        self.cmd.gaitType = 0
        self.cmd.speedLevel = 0
        self.cmd.footRaiseHeight = 0
        self.cmd.bodyHeight = 0
        self.cmd.euler = [0, 0, 0]
        self.cmd.velocity = [0, 0]
        self.cmd.yawSpeed = 0.0
        self.cmd.reserve = 0

    def send_cmd(self, set_cmd):
        self.udp.Recv()
        self.udp.GetRecv(self.state)
        self.reset_cmd()
        set_cmd()
        self.udp.SetSend(self.cmd)
        self.udp.Send()        

    def stop_cmd(self):
        print("stop_cmd")
        self.cmd.mode = 2
        self.cmd.gaitType = 1
        self.cmd.velocity = [0, 0]
        self.cmd.bodyHeight = 0.1

    def walk_cmd(self, vel):
        print("walk_cmd")
        self.cmd.mode = 2
        self.cmd.gaitType = 1
        self.cmd.velocity = [vel, 0]
        self.cmd.bodyHeight = 0.1

    def side_cmd(self, vel):
        print("side_cmd")
        self.cmd.mode = 2
        self.cmd.gaitType = 1
        self.cmd.velocity = [0, vel]
        self.cmd.bodyHeight = 0.1

    def turn_cmd(self, vel):
        print("turn_cmd")
        self.cmd.mode = 2
        self.cmd.gaitType = 2
        self.cmd.velocity[0] = 0.2
        self.cmd.yawSpeed = vel

    def vector_cmd(self, x, y):
        print("vector_cmd")
        self.cmd.mode = 2
        self.cmd.gaitType = 1
        self.cmd.velocity = [x, y]
        self.cmd.bodyHeight = 0.1

    def shutdown(self):
        self.timer.stop()

    def stop(self):
        self.action = lambda: self.stop()
    def walk(self, vel):
        self.action = lambda: self.walk_cmd(vel)
    def side(self, vel):
        self.action = lambda: self.side_cmd(vel)
    def turn(self, vel):
        self.action = lambda: self.turn_cmd(vel)
    def vector(self, x, y):
        self.action = lambda: self.vector_cmd(x, y)

if __name__ == "__main__":
    go1 = Go1()

        
