#from pykeigan_usb.keigan_base import KeiganBase
from keigan_base import KeiganBase

from typing import Tuple
import struct


class KeiganSetting(KeiganBase):
    def __init__(self, port: str, timeout: float = 0.1):
        super().__init__(port, timeout)

        self._maxSpeed = 0.0
        self._minSpeed = 0.0
        self._curveType = 0
        self._acc = 0.0
        self._dec = 0.0
        self._maxTorque = 0.0
        self._qCurrentP = 0.0
        self._qCurrentI = 0.0
        self._qCurrentD = 0.0
        self._speedP = 0.0
        self._speedI = 0.0
        self._speedD = 0.0
        self._positionP = 0.0
        self._interface = 0
        self._ownColor = [0, 0, 0]

    def resetPID(self) -> bool:
        return self.device.sendRequest(0x22, 0, b'')

    def saveAllRegisters(self) -> bool:
        return self.device.sendRequest(0x41, 0, b'')

    def resetAllRegister(self) -> bool:
        return self.device.sendRequest(0x4f, 0, b'')

    def _resetRegister(self, register: int) -> bool:
        return self.device.sendRequest(0x4e, 0, register.to_bytes(1, 'big'))

    def _writeFloatRegister(self, register: int, value: float) -> bool:
        writeData = struct.pack(">f", value)
        return self.device.sendRequest(register, 0, writeData)
    
    def _readFloatRegister(self, register: int) -> Tuple[bool, float]:
        self.device.sendRequest(0x40, 0, register.to_bytes(1, 'big'))
        readData = self.device.recvResponse()

        ret = False
        value = 0.0

        if len(readData) >= 11:
            if readData[1] == 0x40 and readData[4] == register:
                value = struct.unpack(">f", readData[5:9])[0]
                ret = True

        return ret, value

    def getMaxSpeed(self) -> Tuple[bool, float]:
        return self._readFloatRegister(0x02)

    def setMaxSpeed(self, value: float) -> bool:
        return self._writeFloatRegister(0x02, value)

    def resetMaxSpeed(self) -> bool:
        return self._resetRegister(0x02)

    
if __name__ == '__main__':

    import traceback

    try:
        keigan = KeiganSetting(port='/dev/ttyUSB0', timeout=0.1)

        print(f"max speed (default): {keigan.getMaxSpeed()}")

        keigan.setMaxSpeed(100.0)
        print(f"max speed (set=100): {keigan.getMaxSpeed()}")

        keigan.resetMaxSpeed()
        print(f"max speed (reset): {keigan.getMaxSpeed()}")
        
    except:
        traceback.print_exc()