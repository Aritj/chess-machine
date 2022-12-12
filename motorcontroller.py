import pigpio
from time import sleep


class StepperMotorController:
    PULSES = 800
    DIR_PIN = 20
    STEP_PIN = 21

    def __init__(self):
        self.pi = pigpio.pi()
        self.pi.set_mode(self.DIR_PIN, pigpio.OUTPUT)
        self.pi.set_mode(self.STEP_PIN, pigpio.OUTPUT)
        self.pi.set_PWM_dutycycle(self.STEP_PIN, 128)  # PWM 1/2 On 1/2 Off
        self.pi.set_PWM_frequency(self.STEP_PIN, self.PULSES)  # pulses per second

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.pi.set_PWM_dutycycle(self.STEP_PIN, 0)  # PWM off
        self.pi.stop()

    def __position_x(self, x: int) -> None:
        # TODO: map file to x position and set
        pass

    def __position_y(self, y: int) -> None:
        # TODO: map rank to y position and set
        pass

    def __position_z(self, z: int) -> None:
        # TODO: set z positions
        pass

    def __position_reset(self) -> None:
        pass

    def __position_file_and_rank(self, file: str, rank: str) -> None:
        
        pass

    def __grab(self) -> None:
        # TODO: lower magnet, activate electro-magnet, lift magnet
        pass

    def __release(self) -> None:
        # TODO: lower magnet, deactivate electro-magnet, lift magnet
        pass

    def move(self, file_from: str, rank_from: str, file_to: str, rank_to: str) -> None:
        self.test(int(rank_from), int(rank_to))
        print(f'MOVE |{file_from + rank_from}| TO |{file_to + rank_to}|')
        pass
        self.__position_file_and_rank(file_from, rank_from)     # step 1
        self.__grab()                                           # step 2
        self.__position_file_and_rank(file_to, rank_to)         # step 3
        self.__release()                                        # step 4
        self.__position_reset()                                 # step 5

    def test(self, rank_from: int, rank_to: int):
        for _ in range(abs(rank_from - rank_to)):
            sleep(0.25)


if __name__ == "__main__":
    # for unit testing purposes
    with StepperMotorController() as controller:
        controller.move(
            "b", "1",
            "a", "3"
        )
