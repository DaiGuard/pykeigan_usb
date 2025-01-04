import traceback
import serial

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

    com.write(b'\x49\x00\x00\x00\x00')

    readData = b''
    while com.readable():
        tmp = com.read(256)

        if len(tmp) <= 0:
            break

        readData += tmp

    print(readData.decode('utf-8'))


if __name__ == '__main__':

    try:
        main()
    except:
        traceback.print_exc()