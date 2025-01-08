# pykeigan_usb

Keigan motor control library for connected usb

[KeiganMotor KM-1U](https://keigan-motor.com/km-1u/)

![](https://keiganmotor.myshopify.com/cdn/shop/products/fdf_480x352.jpg?v=1575011803)

---

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
        KeiganSetting: maxSpeed
        KeiganSetting: minSpeed
        KeiganSetting: curveType
        KeiganSetting: acc
        KeiganSetting: dec
        KeiganSetting: maxTorque
        KeiganSetting: qCurrentP
        KeiganSetting: qCurrentI
        KeiganSetting: qCurrentD
        KeiganSetting: speedP
        KeiganSetting: speedI
        KeiganSetting: speedD
        KeiganSetting: positionP
        KeiganSetting: interface
        KeiganSetting: ownColor
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

* [ ] CRC16 check enable
* [ ] Read buffer reset slow
* [ ] Unit Test