from pykeigan_usb import KeiganMotorUSB
import time


deviceName = '/dev/ttyUSB0'
keigan = KeiganMotorUSB(deviceName, 0.1)


def test_printInformation():
    ret = keigan.printInformation()
    assert ret == True

