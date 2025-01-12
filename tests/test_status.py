from pykeigan_usb import KeiganMotorUSB
import time


deviceName = '/dev/ttyUSB0'
keigan = KeiganMotorUSB(deviceName, 0.1)


def test_updateStatus():
    ret = keigan.updateStatus()

    assert ret

