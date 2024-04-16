#!/usr/bin/python3
import robot_interface as sdk # type: ignore
from timer import Timer

HIGHLEVEL = 0xee

class Go1():
    def __init__(self):
        self.udp = sdk.UDP(HIGHLEVEL, 8080, "192.168.123.161", 8082)
        self.cmd = sdk.HighCmd()
        self.state = sdk.HighState() 
        self.udp.InitCmdData(self.cmd)

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
        self.cmd.mode = 2
        self.cmd.gaitType = 1
        self.cmd.velocity = [0, 0]
        self.cmd.bodyHeight = 0.1

    def walk_cmd(self, vel):
        self.cmd.mode = 2
        self.cmd.gaitType = 1
        self.cmd.velocity = [vel, 0]
        self.cmd.bodyHeight = 0.1

    def side_cmd(self, vel):
        self.cmd.mode = 2
        self.cmd.gaitType = 1
        self.cmd.velocity = [0, vel]
        self.cmd.bodyHeight = 0.1

    def turn_cmd(self, vel):
        self.cmd.mode = 2
        self.cmd.gaitType = 1
        self.cmd.velocity[0] = 0.2
        self.cmd.yawSpeed = vel

    def vector_cmd(self, x, y, yaw):
        self.cmd.mode = 2
        self.cmd.gaitType = 1
        self.cmd.velocity = [x, y]
        self.cmd.yawSpeed = yaw
        self.cmd.bodyHeight = 0.1

    """ Public API """

    def stop(self):
        self.send_cmd(lambda: self.stop_cmd())
        print("Recieved stop command")
    def walk(self, vel):
        self.send_cmd(lambda: self.walk_cmd(vel)) 
        print("Recieved walk command")
    def side(self, vel):
        self.send_cmd(lambda: self.side_cmd(vel)) 
        print("Recieved side command")
    def turn(self, vel):
        self.send_cmd(lambda: self.turn_cmd(vel)) 
        print("Recieved turn command")
    def vector(self, x, y, yaw):
        self.send_cmd(lambda: self.vector_cmd(x, y, yaw))
        print("Recieved vector command")
    def print_info(self):
        euler = self.state.imu.rpy
        accel = self.state.imu.accelerometer
        print(f"{euler[0]}, {euler[1]}, {euler[2]}")
        print(f"{accel[0]}, {accel[1]}, {accel[2]}")
        return euler, accel

if __name__ == "__main__":
    go1 = Go1()

        
