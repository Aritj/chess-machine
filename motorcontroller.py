import pigpio

from time import sleep
from concurrent.futures import ThreadPoolExecutor

FILE_MAP = {
    "a": 1,
    "b": 2,
    "c": 3,
    "d": 4,
    "e": 5,
    "f": 6,
    "g": 7,
    "h": 8
}

class StepperMotor:
    def __init__(self, dir_pin, step_pin, pulses_hz = 800):
        self.DIR_PIN = dir_pin
        self.STEP_PIN = step_pin
        self.PULSES_HZ = pulses_hz
        self.SLEEP_TIMER = 200 / pulses_hz

        self.pi = pigpio.pi()
        self.pi.set_mode(self.DIR_PIN, pigpio.OUTPUT)
        self.pi.set_mode(self.STEP_PIN, pigpio.OUTPUT)
        self.pi.set_PWM_frequency(self.STEP_PIN, self.PULSES_HZ)  # pulses per second

    def rotate(self, rotations) -> None:
        self.pi.write(self.DIR_PIN, 1 if rotations < 0 else 0) # direction
        self.pi.set_PWM_dutycycle(self.STEP_PIN, 128) # PWM on
        sleep(self.SLEEP_TIMER * abs(rotations))
        self.pi.set_PWM_dutycycle(self.STEP_PIN, 0)  # PWM off

    def close(self) -> None:
        self.pi.stop()

class StepperMotorController:
    __SCALING_VARIABLE: int = 2
    __motors: list[StepperMotor] = []
    __current_file: int = 0
    __current_rank: int = 0

    def __init__(self):
        self.__file_motor = StepperMotor(20, 21)
        #self.__rank_motor = StepperMotor(?, ?)
        self.__motors.append(self.__file_motor)
        #self.__motors.append(self.__rank_motor)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        for motor in self.__motors:
            motor.close()

    def __position_reset(self) -> None:
        self.__file_motor.rotate(-self.__current_file * self.__SCALING_VARIABLE)
        #self.__rank_motor.rotate(-self.__current_rank * self.__SCALING_VARIABLE)

    def __position_file_and_rank(self, file: int, rank: int) -> None:
        file_rotations: int = (file - self.__current_file) * self.__SCALING_VARIABLE
        rank_rotations: int = (rank - self.__current_rank) * self.__SCALING_VARIABLE

        with ThreadPoolExecutor(max_workers = 2) as executor:
            executor.map(self.__file_motor.rotate, (file_rotations,))
            #self.__rank_motor.rotate(rank_rotations)

        self.__current_file = file
        self.__current_rank = rank

    def __grab(self) -> None:
        # TODO: activate electro-magnet
        sleep(0.5)

    def __release(self) -> None:
        # TODO: deactivate electro-magnet
        sleep(0.5)

    def move(self, move: dict) -> None:
        file_from: str = move.get("source")[0]          # a-h (str)
        rank_from: str = move.get("source")[1]          # 1-8 (str)
        file_to: str = move.get("target")[0]            # a-h (str)
        rank_to: str = move.get("target")[1]            # 1-8 (str)

        file_from_mapped: int = FILE_MAP.get(file_from) # 1-8 (int)
        rank_from_mapped: int = int(rank_from)          # 1-8 (int)
        file_to_mapped: int = FILE_MAP.get(file_to)     # 1-8 (int)
        rank_to_mapped: int = int(rank_to)              # 1-8 (int)

        self.__position_file_and_rank(file_from_mapped, rank_from_mapped)
        self.__grab()
        self.__position_file_and_rank(file_to_mapped, rank_to_mapped)
        self.__release()
        self.__position_reset()

if __name__ == "__main__":
    # for unit testing purposes
    with StepperMotorController() as controller:
        controller.move(
            "b", "1",
            "c", "3"
        )