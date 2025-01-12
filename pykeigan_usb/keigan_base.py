from pykeigan_usb.device_usb import DeviceUSB
from typing import Tuple
import struct

class KeiganBase:
    def __init__(self, port: str, timeout: float = 0.1):

        self.device = DeviceUSB(port, timeout)

    def parseErrorCode(self, data: bytes) -> Tuple[bool, int, int]:
        ret = False
        command = -1
        errorCode = -1
        if data[1] == 0xbe:
            ret = True
            command = data[4]
            errorCode = struct.unpack('>I', data[5:9])[0]

        return ret, command, errorCode
            

