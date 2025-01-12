from .keigan_base import KeiganBase

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
        ret = self.device.sendRequest(0x22, 0, b'')
        if not ret:
            return False

        return True

    def saveAllRegisters(self) -> bool:
        return self.device.sendRequest(0x41, 0, b'')

    def resetAllRegister(self) -> bool:
        return self.device.sendRequest(0x4f, 0, b'')

    def _resetRegister(self, register: int) -> bool:
        return self.device.sendRequest(0x4e, 0, register.to_bytes(1, 'big'))

    def _writeFloatRegister(self, register: int, value: float) -> bool:
        writeData = struct.pack(">f", value)
        return self.device.sendRequest(register, 0, writeData)
    
    def _writeByteRegister(self, register: int, value: int) -> bool:
        writeData = struct.pack(">I", value)[3:]
        return self.device.sendRequest(register, 0, writeData)

    def _writeBytesRegister(self, register: int, value: bytes) -> bool:
        writeData = value
        return self.device.sendRequest(register, 0, writeData)

    def _readFloatRegister(self, register: int) -> Tuple[bool, float]:
        ret, readData = self._readRegister(register)
        value = 0.0

        if ret and len(readData) >= 11:
            value = struct.unpack(">f", readData[5:9])[0]
            ret = True
        else:
            ret = False

        return ret, value

    def _readByteRegister(self, register: int) -> Tuple[bool, int]:
        ret, readData = self._readRegister(register)
        value = 0

        if ret and len(readData) >= 8:
            value = readData[5]
            ret = True
        else:
            ret = False

        return ret, value
    
    def _readBytesRegister(self, register: int, size: int) -> Tuple[bool, bytes]:
        ret, readData = self._readRegister(register)
        value = b''        

        if ret and len(readData) >= (7 + size):
            value = readData[5:5+size]
            ret = True
        else:
            ret = False

        return ret, value

    def _readRegister(self, register: int) -> Tuple[bool, bytes]:
        self.device.sendRequest(0x40, 0, register.to_bytes(1, 'big'))
        ret, readData = self.device.recvResponse()

        readData = readData[-1]
        if ret and readData[1] == 0x40 and readData[4] == register:
            ret = True
        else:
            ret = False

        return ret, readData

    def getMaxSpeed(self) -> Tuple[bool, float]:
        return self._readFloatRegister(0x02)

    def setMaxSpeed(self, value: float) -> bool:
        return self._writeFloatRegister(0x02, value)

    def resetMaxSpeed(self) -> bool:
        return self._resetRegister(0x02)

    def getMinSpeed(self) -> Tuple[bool, float]:
        return self._readFloatRegister(0x03)

    def setMinSpeed(self, value: float) -> bool:
        return self._writeFloatRegister(0x03, value)

    def resetMinSpeed(self) -> bool:
        return self._resetRegister(0x03)

    def getCurveType(self) ->Tuple[bool, int]:
        return self._readByteRegister(0x05)
    
    def setCurveType(self, value: int) -> bool:
        return self._writeByteRegister(0x05, value)

    def resetCurveType(self) -> bool:
        return self._resetRegister(0x05)

    def getAcc(self) -> Tuple[bool, float]:
        return self._readFloatRegister(0x07)
    
    def setAcc(self, value: float) -> bool:
        return self._writeFloatRegister(0x07, value)
    
    def resetAcc(self) -> bool:
        return self._resetRegister(0x07)

    def getDec(self) -> Tuple[bool, float]:
        return self._readFloatRegister(0x08)
    
    def setDec(self, value: float) -> bool:
        return self._writeFloatRegister(0x08, value)
    
    def resetDec(self) -> bool:
        return self._resetRegister(0x08)

    def getMaxTorque(self) -> Tuple[bool, float]:
        return self._readFloatRegister(0x0e)
    
    def setMaxTorque(self, value: float) -> bool:
        return self._writeFloatRegister(0x0e, value)
    
    def resetMaxTorque(self) -> bool:
        return self._resetRegister(0x0e)

    def getQCurrentP(self) -> Tuple[bool, float]:
        return self._readFloatRegister(0x18)
    
    def setQCurrentP(self, value: float) -> bool:
        return self._writeFloatRegister(0x18, value)
    
    def resetQCurrentP(self) -> bool:
        return self._resetRegister(0x18)

    def getQCurrentI(self) -> Tuple[bool, float]:
        return self._readFloatRegister(0x19)
    
    def setQCurrentI(self, value: float) -> bool:
        return self._writeFloatRegister(0x19, value)
    
    def resetQCurrentI(self) -> bool:
        return self._resetRegister(0x19)

    def getQCurrentD(self) -> Tuple[bool, float]:
        return self._readFloatRegister(0x1a)
    
    def setQCurrentD(self, value: float) -> bool:
        return self._writeFloatRegister(0x1a, value)
    
    def resetQCurrentD(self) -> bool:
        return self._resetRegister(0x1a)

    def getSpeedP(self) -> Tuple[bool, float]:
        return self._readFloatRegister(0x1b)
    
    def setSpeedP(self, value: float) -> bool:
        return self._writeFloatRegister(0x1b, value)
    
    def resetSpeedP(self) -> bool:
        return self._resetRegister(0x1b)

    def getSpeedI(self) -> Tuple[bool, float]:
        return self._readFloatRegister(0x1c)
    
    def setSpeedI(self, value: float) -> bool:
        return self._writeFloatRegister(0x1c, value)
    
    def resetSpeedI(self) -> bool:
        return self._resetRegister(0x1c)

    def getSpeedD(self) -> Tuple[bool, float]:
        return self._readFloatRegister(0x1d)
    
    def setSpeedD(self, value: float) -> bool:
        return self._writeFloatRegister(0x1d, value)
    
    def resetSpeedD(self) -> bool:
        return self._resetRegister(0x1d)

    def getPositionP(self) -> Tuple[bool, float]:
        return self._readFloatRegister(0x1e)
    
    def setPositionP(self, value: float) -> bool:
        return self._writeFloatRegister(0x1e, value)
    
    def resetPositionP(self) -> bool:
        return self._resetRegister(0x1e)

    def getInterface(self) -> Tuple[bool, int]:
        return self._readByteRegister(0x2e)
    
    def setInterface(self, value: int) -> bool:
        return self._writeByteRegister(0x2e, value)
    
    def resetInterface(self) -> bool:
        return self._resetRegister(0x2e)

    def getOwnColor(self) -> Tuple[bool, int, int, int]:
        ret, data = self._readBytesRegister(0x3a, 3)

        color = [0, 0, 0]

        if len(data) >= 3:
            color[0] = data[0]
            color[1] = data[1]
            color[2] = data[2]
            
        return ret, color[0], color[1], color[2]
    
    def setOwnColor(self, r, g, b) -> bool:

        value = struct.pack(">I", r)[3:] + struct.pack(">I", g)[3:] + struct.pack(">I", b)[3:]

        return self._writeBytesRegister(0x3a, value)
    
    def resetOwnColor(self) -> bool:
        return self._resetRegister(0x3a)


if __name__ == '__main__':

    import traceback

    try:
        keigan = KeiganSetting(port='/dev/ttyUSB0', timeout=0.1)

        print(f"max speed (default): {keigan.getMaxSpeed()}")
        keigan.setMaxSpeed(100.0)
        print(f"max speed (set=100.0): {keigan.getMaxSpeed()}")
        keigan.resetMaxSpeed()
        print(f"max speed (reset): {keigan.getMaxSpeed()}\n")

        print(f"mix speed (default): {keigan.getMinSpeed()}")
        keigan.setMinSpeed(10.0)
        print(f"mix speed (set=10.0): {keigan.getMinSpeed()}")
        keigan.resetMinSpeed()
        print(f"mix speed (reset): {keigan.getMinSpeed()}\n")

        print(f'curve type (default): {keigan.getCurveType()}')
        keigan.setCurveType(0)
        print(f'curve type (set=0): {keigan.getCurveType()}')
        keigan.resetCurveType()
        print(f'curve type (reset): {keigan.getCurveType()}\n')

        print(f'acc (default): {keigan.getAcc()}')
        keigan.setAcc(100.0)
        print(f'acc (set=0): {keigan.getAcc()}')
        keigan.resetAcc()
        print(f'acc (reset): {keigan.getAcc()}\n')

        print(f'dec (default): {keigan.getDec()}')
        keigan.setDec(100.0)
        print(f'dec (set=0): {keigan.getDec()}')
        keigan.resetDec()
        print(f'dec (reset): {keigan.getDec()}\n')

        print(f'max torque (default): {keigan.getMaxTorque()}')
        keigan.setMaxTorque(100.0)
        print(f'max torque (set=0): {keigan.getMaxTorque()}')
        keigan.resetMaxTorque()
        print(f'max torque (reset): {keigan.getMaxTorque()}\n')

        print(f'q current P (default): {keigan.getQCurrentP()}')
        keigan.setQCurrentP(100.0)
        print(f'q current P (set=100.0): {keigan.getQCurrentP()}')
        keigan.resetQCurrentP()
        print(f'q current P (reset): {keigan.getQCurrentP()}\n')

        print(f'q current I (default): {keigan.getQCurrentI()}')
        keigan.setQCurrentI(100.0)
        print(f'q current I (set=100.0): {keigan.getQCurrentI()}')
        keigan.resetQCurrentI()
        print(f'q current I (reset): {keigan.getQCurrentI()}\n')

        print(f'q current D (default): {keigan.getQCurrentD()}')
        keigan.setQCurrentD(100.0)
        print(f'q current P (set=100.0): {keigan.getQCurrentD()}')
        keigan.resetQCurrentD()
        print(f'q current D (reset): {keigan.getQCurrentD()}\n')

        print(f'speed P (default): {keigan.getSpeedP()}')
        keigan.setSpeedP(100.0)
        print(f'speed P (set=100.0): {keigan.getSpeedP()}')
        keigan.resetSpeedP()
        print(f'speed P (reset): {keigan.getSpeedP()}\n')

        print(f'speed I (default): {keigan.getSpeedI()}')
        keigan.setSpeedI(100.0)
        print(f'speed I (set=100.0): {keigan.getSpeedI()}')
        keigan.resetSpeedI()
        print(f'speed I (reset): {keigan.getSpeedI()}\n')

        print(f'speed D (default): {keigan.getSpeedD()}')
        keigan.setSpeedD(100.0)
        print(f'speed D (set=100.0): {keigan.getSpeedD()}')
        keigan.resetSpeedD()
        print(f'speed D (reset): {keigan.getSpeedD()}\n')

        print(f'position P (default): {keigan.getPositionP()}')
        keigan.setPositionP(100.0)
        print(f'position P (set=100.0): {keigan.getPositionP()}')
        keigan.resetPositionP()
        print(f'position P (reset): {keigan.getPositionP()}\n')

        print(f'interface (default): {keigan.getInterface()}\n')

        print(f'own color (default): {keigan.getOwnColor()}')
        keigan.setOwnColor(0, 255, 0)
        print(f'own color (red): {keigan.getOwnColor()}')
        keigan.resetOwnColor()
        print(f'own color (reset): {keigan.getOwnColor()}\n')

        keigan.resetPID()
        keigan.resetAcc()
        keigan.saveAllRegisters()

    except:
        traceback.print_exc()