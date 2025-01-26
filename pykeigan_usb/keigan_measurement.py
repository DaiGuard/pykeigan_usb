from pykeigan_usb.keigan_base import KeiganBase

from logging import getLogger
from typing import Tuple
import struct


class KeiganMeasurement(KeiganBase):
    def __init__(self, port: str, timeout: float = 0.1):
        super().__init__(port, timeout)

    def getMotorMeasurement(self) -> Tuple[bool, float, float, float]:
        """get motor measurement data

        Returns:
            Tuple[bool, float, float, float]: 
                success,
                position [rad],
                velocity [rad/sec],
                torque [N/m]
        """
        ret = False,
        pos = 0.0
        vel = 0.0
        trq = 0.0

        ret = self.device.sendRequest(0xb4, 0, b'')
        ret, readData = self.device.recvResponse()

        readData = readData[-1]
        if ret and readData[1] == 0xb4:
            values = struct.unpack(">fff", readData[2:14])
            
            pos = values[0]
            vel = values[1]
            trq = values[2]
            ret = True
        else:
            ret = False

        return ret, pos, vel, trq

    def getImuMeasurement(self) \
        -> Tuple[bool, int, int, int, int, int, int]:
        """get IMU sensor data

        Returns:
            Tuple[bool, int, int int, int, int, int]: 
                success, 
                accx, accy, accz, 
                gyrox, gyroy, gyroz
        """
        ret = False
        accX = 0
        accY = 0
        accZ = 0
        gyroX = 0
        gyroY = 0
        gyroZ = 0

        ret = self.device.sendRequest(0xb5, 0, b'')
        ret, readData = self.device.recvResponse()

        readData = readData[-1]
        if ret and readData[1] == 0xb5:
            values = struct.unpack(">hhhhhh", readData[2:14])
            
            accX = values[0]
            accY = values[1]
            accZ = values[2]
            gyroX = values[3]
            gyroY = values[4]
            gyroZ = values[5]
            ret = True
        else:
            ret = False

        return ret, accX, accY, accZ, gyroX, gyroY, gyroZ



if __name__ == '__main__':
    import traceback
    import time

    try:
        keigan = KeiganMeasurement('/dev/keiganL', 0.02)

        for i in range(100):
            ret, pos, vel, trq = keigan.getMotorMeasurement()
            if ret:
                print(f"{i}: {pos}, {vel}, {trq}")
            ret, ax, ay, az, gx, gz, gy = keigan.getImuMeasurement()
            if ret:
                print(f"\t{ax}, {ay}, {az}, {gx}, {gy}, {gz}")

            time.sleep(0.03)


    except:
        traceback.print_exc()