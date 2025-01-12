from logging import getLogger
from typing import Tuple, List
import struct
import serial
import re
import binascii


class DeviceUSB:

    def __init__(self, port: str, timeout: float = 0.1) -> None:

        self.logger = getLogger(__name__)

        self.preamble = b'\x00\x00\xaa\xaa'
        self.postamble = b'\x0d\x0a'
        search = self.preamble.hex() + '.*?' + self.postamble.hex()

        self.matchData = re.compile(search)

        self.deviceName = port
        self.baudrate = 115200
        self.timeout = timeout        

        self.deviceCom = serial.Serial(self.deviceName,
                                       baudrate=self.baudrate, bytesize=8,
                                       parity="N", stopbits=1, rtscts=True,
                                       timeout=self.timeout)

        if not self.deviceCom.is_open:
            raise RuntimeError(f'can not open serial device: {self.deviceName}')
        elif not self.deviceCom.writable():
            raise RuntimeError(f'can not write serial device: {self.deviceName}')

    def calcCRC16(self, data) -> bytes:

        crc = struct.unpack('>H', b'\x00\x00')[0]
        polynominal = struct.unpack('>H', b'\x84\x08')[0]
        for d in data:
            tmp = crc ^ d
            for i in range(8):
                if tmp & 1:
                    tmp = tmp >> 1
                    tmp = polynominal ^ tmp
                else:
                    tmp = tmp >> 1

            crc = tmp            

        return crc.to_bytes(2, 'little')

    def sendRequest(self, command: int, task_id: int, values: bytes = b'') -> bool:

        writeData = b''

        writeData += command.to_bytes(1, 'big')
        writeData += task_id.to_bytes(2, 'big')
        writeData += values

        writeData += self.calcCRC16(writeData)
        # writeData += b'\x00\x00'  # dummy CRC16

        ret = self.deviceCom.write(writeData)

        if ret != len(writeData):
            self.logger.error(f'can not send all data: {ret} / {len(writeData)}')
            return False

        return True
    
    def recvResponse(self) -> Tuple[bool, List[bytes]]:

        readData = self.readAll()
        readText = readData.hex()

        ret = True
        res = []

        try:
            dataAllText = self.matchData.findall(readText)

            for dataText in dataAllText:
                data = binascii.unhexlify(dataText)

                crc = self.calcCRC16(data[4:-4])
                if data[-4:-2] == crc:
                    res.append(data[4:-4])                    
                else:
                    self.logger.error(f'crc check error: {data[-4:-2]} / crc')
                    ret = False

        except IndexError:
            self.logger.error(f'recv data size miss match')
            ret = False

        return ret, res

    def readAll(self) -> bytes:

        readData = b''
        while self.deviceCom.readable():
            tmp = self.deviceCom.read(256)
            if len(tmp) <= 0:
                break
            readData += tmp

        return readData
    
    def clearReadBuffer(self) -> None:
        _ = self.readAll()


if __name__ == '__main__':

    import traceback    
    import time
    from logging import basicConfig, DEBUG

    basicConfig(level=DEBUG)

    try:
        device = DeviceUSB('/dev/ttyUSB1', 0.1)

        # Motor enable
        ret = device.sendRequest(0x51, 0, b'')
        if not ret:
            raise RuntimeError('error: send [motor enable]')
        ret, recvData = device.recvResponse()
        if not ret:
            raise RuntimeError('error: recv [motor enable]')

        # Motor speed setting
        ret = device.sendRequest(0x58, 0, struct.pack('>f', 200.0))
        if not ret:
            raise RuntimeError('error: send [motor speed]')
        ret, recvData = device.recvResponse()
        if not ret:
            raise RuntimeError('error: recv [motor speed]')

        # Motor forward rotation
        ret = device.sendRequest(0x60, 0, b'')
        if not ret:
            raise RuntimeError('error: send [motor run foward]')
        ret, recvData = device.recvResponse()
        if not ret:
            raise RuntimeError('error: recv [motor run foward]')

        time.sleep(5.0)

        # Motor disable
        ret = device.sendRequest(0x50, 0, b'')
        if not ret:
            raise RuntimeError('error: send [motor disable]')
        ret, recvData = device.recvResponse()
        if not ret:
            raise RuntimeError('error: recv [motor disable]')

        # Read register
        ret = device.sendRequest(0x40, 0, b'\x02')
        if not ret:
            raise RuntimeError('error: send [read register]')
        ret, readData = device.recvResponse()
        if not ret:
            raise RuntimeError('error: recv [read register]')

        readRegister = readData[0]
        if readRegister[1] == 0x40 and readRegister[4] == 0x02:
            print("* Max Speed")
            print(f'\tReg: {readRegister[4]}')
            print(f'\tVal: {struct.unpack(">f", readRegister[5:9])[0]}')
        else:
            raise RuntimeError('error: read register format')

        # Motor information
        _ = device.clearReadBuffer()
        ret = device.sendRequest(0x49, 0x00, b'\x00\x00')
        if not ret:
            raise RuntimeError('error: send [info]')
        readData = device.readAll()
        print(readData.decode('utf-8'))

    except:        
        traceback.print_exc()