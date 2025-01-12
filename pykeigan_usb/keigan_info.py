from pykeigan_usb.keigan_base import KeiganBase
from logging import getLogger


class KeiganInfo(KeiganBase):
    def __init__(self, port, timeout = 0.1):
        super().__init__(port, timeout)

        self.logger = getLogger(__name__)

    def printInformation(self) -> bool:
        _ = self.device.readAll()
        ret = self.device.sendRequest(0x49, 0, b'\x00\x00')
        if not ret:
            self.logger.error('error send information')
            return False

        readData = self.device.readAll()
        print(readData.decode('utf-8'))

        return True

if __name__ == '__main__':

    import traceback

    try:
        keigan = KeiganInfo(port='/dev/ttyUSB0', timeout=0.1)
        keigan.printInformation()

    except:        
        traceback.print_exc()        