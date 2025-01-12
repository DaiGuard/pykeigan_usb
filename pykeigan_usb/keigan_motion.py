from typing import Tuple
from pykeigan_usb.keigan_base import KeiganBase

import struct


class KeiganMotion(KeiganBase):
    def __init__(self, port: str, timeout: float = 0.1):
        super().__init__(port, timeout)

    def disableMotion(self) -> bool:
        return self.device.sendRequest(0x50, 0, b'')

    def enableMotion(self) -> bool:
        return self.device.sendRequest(0x51, 0, b'')

    def setSpeed(self, velocity: float) -> bool:
        """set motor velocity for run forware, reverse

        Args:
            velocity (float): rad/sec

        Returns:
            bool: success
        """
        writeData = struct.pack('>f', velocity)
        return self.device.sendRequest(0x58, 0, writeData)

    def presetPosition(self, position: float) -> bool:
        """change current position data

        Args:
            position (float): rad

        Returns:
            bool: _description_
        """
        writeData = struct.pack('>f', position)
        return self.device.sendRequest(0x5a, 0, writeData)

    def runForward(self) -> bool:
        return self.device.sendRequest(0x60, 0, b'')

    def runReverse(self) -> bool:
        return self.device.sendRequest(0x61, 0, b'')

    def runAtVelocity(self, velocity: float) -> bool:
        """run constant velocity

        Args:
            velocity (float): rad/sec

        Returns:
            bool: success
        """
        writeData = struct.pack('>f', velocity)
        return self.device.sendRequest(0x62, 0, writeData)

    def moveToPosition(self, position: float) -> bool:
        """move absolute position

        Args:
            position (float): rad

        Returns:
            bool: success
        """
        writeData = struct.pack('>f', position)
        return self.device.sendRequest(0x66, 0, writeData)

    def moveByDistance(self, distance: float) -> bool:
        """move relative position

        Args:
            distance (float): rad

        Returns:
            bool: success
        """
        writeData = struct.pack('>f', distance)
        return self.device.sendRequest(0x68, 0, writeData)

    def freeMotion(self) -> bool:
        return self.device.sendRequest(0x6c, 0, b'')

    def stopMotion(self) -> bool:
        return self.device.sendRequest(0x6d, 0, b'')

    def holdTorque(self) -> bool:
        return self.device.sendRequest(0x72, 0, b'')

    def doTaskset(self) -> bool:
        return self.device.sendRequest(0x81, 0, b'')

    def preparePlaybackMotion(self, index: int, repeating: int, option: int) -> bool:
        writeData = index.to_bytes(1, 'big') + repeating.to_bytes(4, 'big') + option.to_bytes(1, 'big')
        return self.device.sendRequest(0x86, 0, writeData)

    def startPlaybackMotion(self) -> bool:
        return self.device.sendRequest(0x87, 0, b'')

    def stopPlaybackMotion(self) -> bool:
        return self.device.sendRequest(0x88, 0, b'')

    def motoMeasurement(self) -> Tuple[bool, float, float, float]:
        """measurement current position, velocity, torque

        Returns:
            Tuple[bool, float, float, float]: 
                success,
                position [rad]
                velocity [rad/s]
                torque [Nm]
        """
        ret = self.device.sendRequest(0xb4, 0, b'')
        if not ret:
            return False, 0.0, 0.0, 0.0
        
        ret, readData = self.device.recvResponse()
        if not ret:
            return False, 0.0, 0.0, 0.0

        readData = readData[-1]

        position = struct.unpack('>f', readData[2:6])[0]
        velocity = struct.unpack('>f', readData[6:10])[0]
        torque = struct.unpack('>f', readData[10:14])[0]

        return True, position, velocity, torque


if __name__ == '__main__':

    import traceback
    import time
    
    try:
        keigan = KeiganMotion(port='/dev/ttyUSB1', timeout=0.1)

        keigan.enableMotion()

        keigan.setSpeed(20.0)
        keigan.runForward()
        time.sleep(5)
        keigan.runReverse()
        time.sleep(5)
        keigan.stopMotion()
        time.sleep(3)

        keigan.runAtVelocity(1.0)
        time.sleep(5)
        keigan.runAtVelocity(5.0)
        time.sleep(5)
        keigan.runAtVelocity(10.0)
        time.sleep(5)
        keigan.runAtVelocity(20.0)
        time.sleep(5)
        keigan.runAtVelocity(10.0)
        time.sleep(5)
        keigan.runAtVelocity(5.0)
        time.sleep(5)
        keigan.runAtVelocity(1.0)
        time.sleep(5)
        keigan.runAtVelocity(-1.0)
        time.sleep(5)
        keigan.runAtVelocity(-5.0)
        time.sleep(5)
        keigan.runAtVelocity(-10.0)
        time.sleep(5)
        keigan.runAtVelocity(-20.0)
        time.sleep(5)
        keigan.runAtVelocity(-10.0)
        time.sleep(5)
        keigan.runAtVelocity(-5.0)
        time.sleep(5)
        keigan.runAtVelocity(-1.0)
        time.sleep(5)
        keigan.stopMotion()
        time.sleep(3)

        keigan.disableMotion()


    except:
        traceback.print_exc()