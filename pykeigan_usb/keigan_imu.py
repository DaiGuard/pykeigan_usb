from pykeigan_usb.keigan_base import KeiganBase

from logging import getLogger


class KeiganIMU(KeiganBase):
    def __init__(self, port: str, timeout: float = 0.1):
        super().__init__(port, timeout)

    def enableIMU(self) -> bool:
        return self.device.sendRequest(0xea, 0, b'')

    def disableIMU(self) -> bool:
        return self.device.sendRequest(0xeb, 0, b'')


if __name__ == '__main__':
    import traceback

    try:
        keigan = KeiganIMU('/dev/keiganL', 0.02)

        # ret = keigan.enableIMU()
        # if not ret:
        #     print("imu enable failed")

        ret = keigan.disableIMU()
        if not ret:
            print("imu disable failed")
    
    except:
        traceback.print_exc()
