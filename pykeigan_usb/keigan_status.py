#from pykeigan_usb.keigan_base import KeiganBase
from keigan_base import KeiganBase


class KeiganStatus(KeiganBase):
    def __init__(self, port: str, timeout: float = 0.1):
        super().__init__(port, timeout)

        # True: enable checksum, False: disable checksum
        self.enableCheckSum = False

        # True: enable IMU, False: disable IMU
        self.enableIMU = False
        
        # True: enable motor measurement, False: disable motor measurement
        self.enableMotorMeas = False

        # True: queue paused, Flase: queue resumed
        self.stateMotorQueue = False

        # True: motor enabled, False: motor disabled
        self.enableMotor = False

        # 0: raedy, 
        # 1: teaching prepare, 2: teaching doing, 
        # 3: playback prepare, 4: playback doing
        # 5: playgack pause, 6: playback recording
        # 7: taskset doing, 8, taskset pausing
        # 20 imu using
        self.stateFlashMem = 0

        # 0: none, 1, velocity, 2: position, 3: torque, 255: others
        self.modeMotorControl = 0

    def updateStatus(self):

        self.device.sendRequest(0x9a, 0x0000, b'')
        readData = self.device.recvResponse()

        field_size = readData[0]
        data_type = readData[1]
        values = readData[5:-2]
        
        self.enableMotor = values[0] & 0x01 > 0
        self.stateMotorQueue = values[0] & 0x02 > 0
        self.enableMotorMeas = values[0] & 0x04 > 0
        self.enableIMU = values[0] & 0x08 > 0
        self.enableCheckSum = values[0] & 0x80 > 0

        self.stateFlashMem = values[1]
        self.modeMotorControl = values[2]
        


if __name__ == '__main__':

    import traceback
    import struct

    try:
        keigan = KeiganStatus(port='/dev/ttyUSB0', timeout=0.1)

        # keigan.device.sendRequest(0x51, 0, b'')
        # keigan.device.sendRequest(0xea, 0, b'')
        # keigan.device.sendRequest(0x58, 0, struct.pack('>f', 200.0))
        # keigan.device.sendRequest(0x60, 0, b'')
        # keigan.device.sendRequest(0x50, 0, b'')

        keigan.updateStatus()

        print("motor enable: ", keigan.enableMotor)
        print("queue state : ", keigan.stateMotorQueue)
        print("motor meas enable : ", keigan.enableMotorMeas)
        print("imu enable : ", keigan.enableIMU)
        print("checksum enable : ", keigan.enableCheckSum)
        print("state flash memory : ", keigan.stateFlashMem)
        print("mode motor ctrl : ", keigan.modeMotorControl)

    except:        
        traceback.print_exc()        