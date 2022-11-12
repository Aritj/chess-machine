import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime
from random import shuffle


FILE_TO_X_MAP = {
    "a": 0,
    "b": 1,
    "c": 2,
    "d": 3,
    "e": 4,
    "f": 5,
    "g": 6,
    "h": 7,
    "a": 8
}

RANK_TO_Y_MAP = {
    "0": 0,
    "1": 0,
    "2": 0,
    "3": 0,
    "4": 0,
    "5": 0,
    "6": 0,
    "7": 0,
    "8": 8
}

START_POSITION = {
    "x": 0,
    "y": 0,
    "z": 0
}


class StepperMotorController:
    GPIO_LIST: list[int] = [12, 16, 18, 22]

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.GPIO_LIST, GPIO.OUT)
        GPIO.output(self.GPIO_LIST, GPIO.LOW)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        GPIO.cleanup()

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
        self.__position_x(START_POSITION.get("x"))
        self.__position_y(START_POSITION.get("y"))
        self.__position_z(START_POSITION.get("z"))

    def __position_file_and_rank(self, file: str, rank: str) -> None:
        self.__position_x(FILE_TO_X_MAP.get(file))
        self.__position_y(RANK_TO_Y_MAP.get(rank))

    def __grab(self) -> None:
        # TODO: lower magnet, activate electro-magnet, lift magnet
        pass

    def __release(self) -> None:
        # TODO: lower magnet, deactivate electro-magnet, lift magnet
        pass

    def move(self, file_from: str, rank_from: str, file_to: str, rank_to: str) -> None:
        # self.test()
        print(f'MOVE |{file_from + rank_from}| TO |{file_to + rank_to}|')
        pass
        self.__position_file_and_rank(file_from, rank_from)     # step 1
        self.__grab()                                           # step 2
        self.__position_file_and_rank(file_to, rank_to)         # step 3
        self.__release()                                        # step 4
        self.__position_reset()                                 # step 5

    def test(self):
        seq = [
            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 1],
            [1, 0, 0, 1]
        ]

        for _ in range(512):
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(self.GPIO_LIST[pin], seq[halfstep][pin])
                sleep(0.001)


if __name__ == "__main__":
    # for unit testing purposes
    with StepperMotorController() as controller:
        controller.move(
            "b", "1",
            "a", "3"
        )
