import traceback
import serial
import time
import struct


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

    # モーターEnable
    com.write(b'\x51\x00\x00\x00\x00')

    # モーター速度設定
    com.write(b'\x58\x00\x01' + struct.pack('>f', 500.0) + b'\x00\x00')

    # モーター回転
    com.write(b'\x60\x00\x00\x00\x00')

    time.sleep(5.0)

    # モーターDisable
    com.write(b'\x50\x00\x00\x00\x00')


if __name__ == '__main__':

    try:
        main()
    except:
        traceback.print_exc()