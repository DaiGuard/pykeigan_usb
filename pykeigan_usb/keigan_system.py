from .keigan_base import KeiganBase


class KeiganSystem(KeiganBase):

    def __init__(self, port, timeout = 0.1):
        super().__init__(port, timeout)

    def enableChecksum(self) -> bool:
        return self.device.sendRequest(0xf3, 0, int(1).to_bytes(1, 'big'))
    
    def disableChecksum(self) -> bool:
        return self.device.sendRequest(0xf3, 0, int(0).to_bytes(1, 'big'))
    
    def reboot(self) -> bool:
        return self.device.sendRequest(0xf0, 0, b'')
    
    def enterDeviceFirmwareUpdate(self) -> bool:
        return self.device.sendRequest(0xfd, 0, b'')