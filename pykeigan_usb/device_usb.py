import serial
import re


class DeviceUSB:

    def __init__(self, port: str, timeout: float = 0.1) -> None:

        self.preamble = b'\x00\x00\xaa\xaa'
        self.postamble = b'\x0d\x0a'

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
        
    def sendRequest(self, command: int, task_id: int, values: bytes) -> bool:

        writeData = b''

        writeData += command.to_bytes(1, 'big')
        writeData += task_id.to_bytes(2, 'big')
        writeData += values
        writeData += b'\x00\x00'  # dummy CRC16

        ret = self.deviceCom.write(writeData)

        if ret != len(writeData):
            return False

        return True
    
    def recvResponse(self) -> bytes:

        readData = self.readAll()

        search = self.preamble + b'.*?' + self.postamble
        data = re.findall(search, readData)[-1]

        return data[4:-2]

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
    import struct
    import time    

    try:
        device = DeviceUSB('/dev/ttyUSB0', 0.1)

        # Motor enable
        device.sendRequest(0x51, 0, b'')

        # Motor speed setting
        device.sendRequest(0x58, 0, struct.pack('>f', 200.0))

        # Motor forward rotation
        device.sendRequest(0x60, 0, b'')

        time.sleep(5.0)

        # Motor disable
        device.sendRequest(0x50, 0, b'')

        # Write register
        device.sendRequest(0x02, 0, struct.pack('>f', 200.0))

        # Read register
        device.sendRequest(0x40, 0, b'\x02')
        readData = device.recvResponse()

        print("* Max Speed")
        print(f'\tReg: {readData[4]}')
        print(f'\tVal: {struct.unpack(">f", readData[5:9])[0]}')

        # # Motor information
        # _ = device.clearReadBuffer()
        # device.sendRequest(0x49, 0x00, b'\x00\x00')
        # readData = device.readAll()
        # print(readData.decode('utf-8'))

    except:        
        traceback.print_exc()