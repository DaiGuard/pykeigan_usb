from .keigan_base import KeiganBase


class KeiganLED(KeiganBase):
    def __init__(self, port: str, timeout: float = 0.1):
        super().__init__(port, timeout)

        # [r, g, b]
        self.color = [0, 255, 0]

        # 0: off, 1: on, 2: blinking, 3: flickering
        self.mode = 1

    def setColor(self, color: list) -> None:
        self.color = color
        self.updateLED()
        
    def setMode(self, mode: int) -> None:
        self.mode = mode
        self.updateLED()

    def updateLED(self):

        values = b''
        values += self.mode.to_bytes(1, 'big')
        values += self.color[0].to_bytes(1, 'big')
        values += self.color[1].to_bytes(1, 'big')
        values += self.color[2].to_bytes(1, 'big')

        self.device.sendRequest(0xe0, 0, values)




if __name__ == '__main__':

    import traceback
    import time

    try:
        keigan = KeiganLED(port='/dev/ttyUSB0', timeout=0.1)

        print("LED color: RED")
        keigan.setColor([255,   0,   0])
        time.sleep(3)
        print("LED color: GREEN")
        keigan.setColor([  0, 255,   0])
        time.sleep(3)
        print("LED color: BLUE")
        keigan.setColor([  0,   0, 255])
        time.sleep(3)

        print("LED mode: OFF")
        keigan.setMode(0)
        time.sleep(3)
        print("LED mode: ON")
        keigan.setMode(1)
        time.sleep(3)
        print("LED mode: BLINKING")
        keigan.setMode(2)
        time.sleep(3)
        print("LED mode: FLIKERING")
        keigan.setMode(3)
        time.sleep(3)

        keigan.setColor([  0, 255,   0])
        keigan.setMode(3)

    except:
        traceback.print_exc()