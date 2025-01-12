from pykeigan_usb.keigan_base import KeiganBase
from logging import getLogger

class KeiganLED(KeiganBase):
    def __init__(self, port: str, timeout: float = 0.1):
        super().__init__(port, timeout)

        self.logger = getLogger(__name__)

        # [r, g, b]
        self.color = [0, 255, 0]

        # 0: off, 1: on, 2: blinking, 3: flickering
        self.mode = 1

    def setLEDColor(self, color: list) -> bool:
        """change LED color

        Args:
            color (list): [red, green, blue]

        Returns:
            bool: success
        """
        self.color = color
        return self.updateLED()
        
    def setLEDMode(self, mode: int) -> bool:
        """change LED mode

        Args:
            mode (int): 0=OFF,1=SOLID,2=FLASH,3=DIM

        Returns:
            bool: success
        """
        self.mode = mode
        return self.updateLED()

    def updateLED(self) -> bool:

        values = b''
        values += self.mode.to_bytes(1, 'big')
        values += self.color[0].to_bytes(1, 'big')
        values += self.color[1].to_bytes(1, 'big')
        values += self.color[2].to_bytes(1, 'big')

        ret = self.device.sendRequest(0xe0, 0, values)
        if not ret:
            self.logger.error('error send led status')
            return False

        ret, recvData = self.device.recvResponse()
        if not ret:
            self.logger.error('error recv led status')
            return False

        ret, cmd, err = self.parseErrorCode(recvData[-1])
        if not ret or ret and err > 0:
            self.logger.error(f'response error : [{err}]')
            return False

        return True


if __name__ == '__main__':

    import traceback
    import time

    try:
        keigan = KeiganLED(port='/dev/ttyUSB0', timeout=0.1)

        print("LED color: RED")
        keigan.setLEDColor([255,   0,   0])
        time.sleep(3)
        print("LED color: GREEN")
        keigan.setLEDColor([  0, 255,   0])
        time.sleep(3)
        print("LED color: BLUE")
        keigan.setLEDColor([  0,   0, 255])
        time.sleep(3)

        print("LED mode: OFF")
        keigan.setLEDMode(0)
        time.sleep(3)
        print("LED mode: ON")
        keigan.setLEDMode(1)
        time.sleep(3)
        print("LED mode: BLINKING")
        keigan.setLEDMode(2)
        time.sleep(3)
        print("LED mode: FLIKERING")
        keigan.setLEDMode(3)
        time.sleep(3)

        keigan.setLEDColor([  0, 255,   0])
        keigan.setLEDMode(3)

    except:
        traceback.print_exc()