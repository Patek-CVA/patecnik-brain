from machine import PWM, Pin

PWM_FREQUENCY: int = 50  # Hz


class Motor:
    def __init__(self,
                 pwm: int,
                 in_1: int,
                 in_2: int,
                 standby: int):
        self.pwm: PWM = PWM(Pin(pwm), freq=PWM_FREQUENCY)
        self.in_1: Pin = Pin(in_1, mode=Pin.OUT, pull=None)
        self.in_2: Pin = Pin(in_2, mode=Pin.OUT, pull=None)
        self.stby: Pin = Pin(standby, mode=Pin.OUT, pull=None)
        self._standby()

    def _standby(self) -> None:
        self.stby.off()

    def __prepare_movement(self, speed: int) -> None:
        self.pwm.duty_u16(map_speed(speed))
        self.stby.on()

    def forwards(self, speed: int) -> None:
        """
        Start moving forwards.
        :param speed: the motor movement speed (between 0 and 100)
        :return: None
        """
        self.__prepare_movement(speed)
        self.in_1.on()
        self.in_2.off()

    def backwards(self, speed: int) -> None:
        """
        Start moving backwards.
        :param speed: the motor movement speed (between 0 and 100)
        :return: None
        """
        self.__prepare_movement(speed)
        self.in_1.off()
        self.in_2.on()

    def stop(self) -> None:
        """
        Stop the motor and enable standby mode.
        :return: None
        """
        self._standby()
        self.in_1.off()
        self.in_2.off()
        self.pwm.duty_u16(0)


def map_speed(speed: int) -> int:
    """
    Maps 0 - 100 speed to 0 - 65535 speed.
    :param speed: the original speed value
    :return: the mapped speed value
    """
    if speed < 0 or speed > 100:
        raise ValueError("Speed must be between 0 and 100!")
    return int(speed * 655.35)
