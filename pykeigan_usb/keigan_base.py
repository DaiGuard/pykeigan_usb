from .device_usb import DeviceUSB

class KeiganBase:
    def __init__(self, port: str, timeout: float = 0.1):

        self.device = DeviceUSB(port, timeout)

