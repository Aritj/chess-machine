from pigpio import pi, OUTPUT, HIGH, LOW

from time import sleep

class ElectroMagnet:
    def __init__(self, sig_pin):
        self.__SIG_PIN = sig_pin
        self.__PI = pi()

        self.__PI.set_mode(self.__SIG_PIN, OUTPUT)

    def activate(self):
        self.__PI.write(self.__SIG_PIN, HIGH)

    def deactivate(self):
        self.__PI.write(self.__SIG_PIN, LOW)

    def close(self):
        self.__PI.stop()


class ServoMotor:
    def __init__(self, pwm_pin: int):
        self.__PWM_PIN = pwm_pin
        self.__PI = pi()

        self.__PI.set_mode(self.__PWM_PIN, OUTPUT)

    def __set_PWM(self, pulsewidth: int):
        SLEEP_TIMER: float = 1

        self.__PI.set_servo_pulsewidth(self.__PWM_PIN, pulsewidth)
        sleep(SLEEP_TIMER)
        self.__PI.set_servo_pulsewidth(self.__PWM_PIN, 0)

    def max(self):
        self.__set_PWM(2450) # 2500 most clockwise

    def min(self):
        self.__set_PWM(500) # 500 most counter-clockwise

    def close(self):
        self.__PI.stop()


class StepperMotor:
    __scaling_factor: float = 1.0
    __PULSE_HZ: int = 800

    def __init__(self, dir_pin: int, step_pin: int, steps_per_revolution: int = 200):
        self.__DIR_PIN = dir_pin
        self.__STEP_PIN = step_pin
        self.__STEPS_PER_REVOLUTION = steps_per_revolution  # 360 / step angle

        self.__PI = pi()
        self.__PI.set_mode(self.__DIR_PIN, OUTPUT)
        self.__PI.set_mode(self.__STEP_PIN, OUTPUT)

    def set_scale(self, scaling_factor: float):
        self.__scaling_factor = scaling_factor

    def rotate(self, rotations: int) -> None:
        SLEEP_TIMER = (self.__STEPS_PER_REVOLUTION / self.__PULSE_HZ) * abs(rotations) * self.__scaling_factor

        self.__PI.set_PWM_frequency(self.__STEP_PIN, self.__PULSE_HZ)
        self.__PI.write(self.__DIR_PIN, HIGH if rotations > 0 else LOW)  # set direction
        self.__PI.set_PWM_dutycycle(self.__STEP_PIN, 128)  # start rotation
        sleep(SLEEP_TIMER) # sleep until x rotations have been completed
        self.__PI.set_PWM_dutycycle(self.__STEP_PIN, 0)  # stop rotation

    def close(self) -> None:
        self.__PI.stop()