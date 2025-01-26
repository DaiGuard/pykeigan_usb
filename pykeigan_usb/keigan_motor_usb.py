from pykeigan_usb.keigan_info import KeiganInfo
from pykeigan_usb.keigan_setting import KeiganSetting
from pykeigan_usb.keigan_status import KeiganStatus
from pykeigan_usb.keigan_led import KeiganLED
from pykeigan_usb.keigan_motion import KeiganMotion
from pykeigan_usb.keigan_system import KeiganSystem
from pykeigan_usb.keigan_measurement import KeiganMeasurement


class KeiganMotorUSB(KeiganInfo, KeiganSetting, KeiganStatus, KeiganLED, KeiganMotion, KeiganSystem, KeiganMeasurement):
    def __init__(self, port, timeout = 0.1):
        super().__init__(port, timeout)


if __name__ == '__main__':

    import traceback

    try:
        keigan = KeiganMotorUSB(port='/dev/ttyUSB0', timeout=0.1)

        keigan.printInformation()

    except:        
        traceback.print_exc()            