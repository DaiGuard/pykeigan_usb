<img src="https://github.com/DaiGuard/pykeigan_usb/actions/workflows/python-package.yml/badge.svg" />

# pykeigan_usb

Keigan motor control library for connected usb

[KeiganMotor KM-1U](https://keigan-motor.com/km-1u/)

<img src="https://keiganmotor.myshopify.com/cdn/shop/products/fdf_480x352.jpg?v=1575011803" width="30%">

---

### data format

- request data format

    | command  | task id  | values    | crc16   |
    | ---      | ---     | ---       | ---     |
    | 1 bytes  | 1 bytes | 0~n bytes | 2 bytes |

- response data format

    | priamble               | len     | tx type | values    | crc16   | postamble  |
    | ---                    | ---     | ---     | ---       | ---     | ---        |
    | 4 bytes                | 1 bytes | 1 bytes | 0~n bytes | 2 bytes | 2 bytes    |
    | 0x00, 0x00, 0xAA, 0xAA |         |         |           |         | 0x0D, 0x0A |    

### crc16 format

The CRC check used is [CRC-16/KERMIT](https://crccalc.com/?crc=123456789&method=CRC-16/KERMIT&datatype=ascii&outtype=hex)

initial data = [ 0x00, 0x00 ], polynominal = [ 0x84, 0x08 ]

### examples

```python
from pykeigan_usb import KeiganMotorUSB
import time


keigan = KeiganMotorUSB(port='/dev/ttyUSB0', timeout=0.1)

keigan.enableMotion()

keigan.setSpeed(100.0)
keigan.runForward()
time.sleep(5)
keigan.stopMotion()

keigan.disableMotion()

```

### class diagram

```mermaid
classDiagram
    class KeiganBase
        <<Abstract>> KeiganBase
        KeiganBase: device

    class DeviceUSB
        DeviceUSB
        DeviceUSB: deviceName
        DeviceUSB: deviceCom
        DeviceUSB: sendRequest(command, task_id, values) -> bool
        DeviceUSB: recvResponse(command, task_id) -> bytes
        DeviceUSB: readAll() -> bytes
        DeviceUSB: clearReadBuffer()

    class KeiganInfo
        KeiganInfo
        KeiganInfo: printInformation()

    class KeiganStatus
        KeiganStatus
        KeiganStatus: enableCheckSum
        KeiganStatus: enableIMU
        KeiganStatus: enableMotorMeas
        KeiganStatus: stateMotorQueue
        KeiganStatus: enableMotor
        KeiganStatus: stateFlashMem
        KeiganStatus: modeMotorControl
        KeiganStatus: updateStatus()

    class KeiganLED
        KeiganLED
        KeiganLED: color
        KeiganLED: mode
        KeiganLED: setColor(color)
        KeiganLED: setMode(mode)

    class KeiganSetting
        KeiganSetting
        KeiganSetting: resetPID()
        KeiganSetting: saveAllRegisters()
        KeiganSetting: resetAllRegisters()
        KeiganSetting: getMaxSpeed() -> float
        KeiganSetting: setMaxSpeed(value)
        KeiganSetting: resetMaxSpeed()
        KeiganSetting: getMinSpeed() -> float
        KeiganSetting: setMinSpeed(value)
        KeiganSetting: resetMinSpeed()
        KeiganSetting: getCurveType() -> int
        KeiganSetting: setCurveType(value)
        KeiganSetting: resetCurveType()
        KeiganSetting: getAcc() -> float
        KeiganSetting: setAcc(value)
        KeiganSetting: resetAcc()
        KeiganSetting: getDec() -> float
        KeiganSetting: setDec(value)
        KeiganSetting: resetDec()
        KeiganSetting: getMaxTorque() -> float
        KeiganSetting: setMaxTorque(value)
        KeiganSetting: resetMaxTorque()
        KeiganSetting: getQCurrentP() -> float
        KeiganSetting: setQCurrentP(value)
        KeiganSetting: resetQCurrentP()
        KeiganSetting: getQCurrentI() -> float
        KeiganSetting: setQCurrentI(value)
        KeiganSetting: resetQCurrentI()
        KeiganSetting: getQCurrentD() -> float
        KeiganSetting: setQCurrentD(value)
        KeiganSetting: resetQCurrentD()
        KeiganSetting: getSpeedP() -> float
        KeiganSetting: setSpeedP(value)
        KeiganSetting: resetSpeedP()
        KeiganSetting: getSpeedI() -> float
        KeiganSetting: setSpeedI(value)
        KeiganSetting: resetSpeedI()
        KeiganSetting: getSpeedD() -> float
        KeiganSetting: setSpeedD(value)
        KeiganSetting: resetSpeedD()
        KeiganSetting: getPositionP() -> float
        KeiganSetting: setPositionP(value)
        KeiganSetting: resetPositionP()
        KeiganSetting: getInterface() -> int
        KeiganSetting: setInterface(value)
        KeiganSetting: resetInterface()
        KeiganSetting: getOwnColor() -> int
        KeiganSetting: setOwnColor(value)
        KeiganSetting: resetOwnColor()

    class KeiganMotion
        KeiganMotion
        KeiganMotion: disableMotion()
        KeiganMotion: enableMotion()
        KeiganMotion: setSpeed(velocity)
        KeiganMotion: presetPosition(position)
        KeiganMotion: runForward()
        KeiganMotion: runReverse()
        KeiganMotion: runAtVelocity(velocity)
        KeiganMotion: moveToPosition(potision)
        KeiganMotion: moveByDistance(distance)
        KeiganMotion: freeMotion()
        KeiganMotion: stopMotion()
        KeiganMotion: holdTorque()
        KeiganMotion: doTaskset()
        KeiganMotion: preparePlaybackMotion(index, repeating, option)
        KeiganMotion: startPlaybackMotion()
        KeiganMotion: stopPlaybackMotion()

    class KeiganSystem
        KeiganSystem
        KeiganSystem: enableChecksum()
        KeiganSystem: disableChecksum()
        KeiganSystem: reboot()
        KeiganSystem: enterDeviceFirmwareUpdate()

    KeiganMotorUSB <|.. KeiganInfo
    KeiganMotorUSB <|.. KeiganStatus
    KeiganMotorUSB <|.. KeiganSetting
    KeiganMotorUSB <|.. KeiganMotion
    KeiganMotorUSB <|.. KeiganLED
    KeiganMotorUSB <|.. KeiganSystem

    KeiganInfo <|-- KeiganBase
    KeiganStatus <|-- KeiganBase
    KeiganSetting <|-- KeiganBase
    KeiganMotion <|-- KeiganBase
    KeiganLED <|-- KeiganBase
    KeiganSystem <|-- KeiganBase

    KeiganBase o-- DeviceUSB
```

### To-Do

* [x] python package pip install
* [x] CRC16 check enable
* [ ] response check
* [ ] Read buffer reset slow
* [ ] Unit Test