import traceback
import serial
import time
import struct
import re

def main():
    
    deviceName = '/dev/ttyUSB0'

    com = serial.Serial(deviceName,
                        baudrate=115200, bytesize=8,
                        parity="N", stopbits=1, rtscts=True,
                        timeout=3.0)
    if not com.is_open:
        raise RuntimeError(f'can not open serial device: {deviceName}')
    elif not com.writable():
        raise RuntimeError(f'can not write serial device: {deviceName}')

    # # モーターEnable
    # com.write(b'\x51\x00\x00\x00\x00')

    # レジスタ読み取り
    com.write(b'\x40\x00\x00\x02\x00\x00')
    readData = b''    
    while com.readable():
        tmp = com.read()
        if len(tmp) <= 0:
            break
        readData += tmp
    data = re.findall(b'\t([^\r\n]+)\r\n', readData)[-1]
    value = struct.unpack('>f', data[4:8])[0]
    print("* Max Speed (Before)")
    print(f'\t{readData}')
    print(f'\t{data}')
    print(f'\t{value}')

    # # レジスタ書込み
    # com.write(b'\x02\x00\x00' + struct.pack('>f', 500.0) + b'\x00\x00')

    # # レジスタ読み取り
    # com.write(b'\x40\x00\x00\x02\x00\x00')
    # readData = b''    
    # while com.readable():
    #     tmp = com.read()
    #     if len(tmp) <= 0:
    #         break
    #     readData += tmp
    # data = re.findall(b'\t([^\r\n]+)\r\n', readData)[-1]
    # value = struct.unpack('>f', data[4:8])[0]
    # print("* Max Speed (After)")
    # print(f'\t{readData}')
    # print(f'\t{data}')
    # print(f'\t{value}')

    # # モーターEnable
    # com.write(b'\x02\x00\x00\x00\x00')

    # # モーター速度設定
    # com.write(b'\x58\x00\x01' + struct.pack('>f', 200.0) + b'\x00\x00')

    # # モーター回転
    # com.write(b'\x60\x00\x00\x00\x00')

    # time.sleep(5.0)

    # # モーターDisable
    # com.write(b'\x50\x00\x00\x00\x00')


if __name__ == '__main__':

    try:
        main()
    except:
        traceback.print_exc()