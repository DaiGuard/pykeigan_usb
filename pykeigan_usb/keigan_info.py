#from pykeigan_usb.keigan_base import KeiganBase
from keigan_base import KeiganBase


class KeiganInfo(KeiganBase):
    def __init__(self, port, timeout = 0.1):
        super().__init__(port, timeout)

    def printInformation(self) -> None:
        _ = self.device.readAll()
        self.device.sendRequest(0x49, 0, b'\x00\x00')
        readData = self.device.readAll()
        print(readData.decode('utf-8'))

if __name__ == '__main__':

    import traceback

    try:
        keigan = KeiganInfo(port='/dev/ttyUSB0', timeout=0.1)

        keigan.printInformation()

    except:        
        traceback.print_exc()        