from .keigan_info import KeiganInfo
from .keigan_setting import KeiganSetting
from .keigan_status import KeiganStatus
from .keigan_led import KeiganLED
from .keigan_motion import KeiganMotion
from .keigan_system import KeiganSystem

class KeiganMotorUSB(KeiganInfo, KeiganSetting, KeiganStatus, KeiganLED, KeiganMotion, KeiganSystem):
    def __init__(self, port, timeout = 0.1):
        super().__init__(port, timeout)


if __name__ == '__main__':

    import traceback

    try:
        keigan = KeiganMotorUSB(port='/dev/ttyUSB0', timeout=0.1)

        keigan.printInformation()

    except:        
        traceback.print_exc()            