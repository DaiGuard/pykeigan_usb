from pykeigan_usb import KeiganMotorUSB
import time


deviceName = '/dev/ttyUSB0'
keigan = KeiganMotorUSB(deviceName, 0.1)


def test_setLEDColor():
    ret1 = keigan.setLEDColor([255, 0, 0])
    time.sleep(1)
    ret2 = keigan.setLEDColor([0, 0, 255])
    time.sleep(1)
    ret3 = keigan.setLEDColor([0, 255, 0])
    time.sleep(1)        

    assert ret1 and ret2 and ret3

def test_setLEDMode():
    ret1 = keigan.setLEDMode(0)
    time.sleep(3)
    ret2 = keigan.setLEDMode(2)
    time.sleep(3)
    ret3 = keigan.setLEDMode(3)
    time.sleep(3)
    ret4 = keigan.setLEDMode(1)

    assert ret1 and ret2 and ret3 and ret4
