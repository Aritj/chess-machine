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

class Magnet:
    def __init__(self, sig_pin):
        self.__SIG_PIN = sig_pin
        self.__PI = pigpio.pi()

        self.__PI.set_mode(self.__SIG_PIN, pigpio.OUTPUT)

    def activate(self):
        self.__PI.write(self.__SIG_PIN, pigpio.HIGH)

    def deactivate(self):
        self.__PI.write(self.__SIG_PIN, pigpio.LOW)
    
    def close(self):
        self.__PI.stop()



class StepperMotor:
    def __init__(self, dir_pin: int, step_pin: int, steps_per_revolution: int = 200):
        self.__DIR_PIN = dir_pin
        self.__STEP_PIN = step_pin
        self.__STEPS_PER_REVOLUTION = steps_per_revolution # 360 / step angle

        self.__PI = pigpio.pi()
        self.__PI.set_mode(self.__DIR_PIN, pigpio.OUTPUT)
        self.__PI.set_mode(self.__STEP_PIN, pigpio.OUTPUT)

    def rotate(self, rotations: int, pulse_hz: int = 800) -> None:
        SCALING_FACTOR: int = 1
        SLEEP_TIMER = (self.__STEPS_PER_REVOLUTION / pulse_hz) * abs(rotations) * SCALING_FACTOR

        self.__PI.set_PWM_frequency(self.__STEP_PIN, pulse_hz)
        self.__PI.write(self.__DIR_PIN, pigpio.HIGH if rotations < 0 else pigpio.LOW)  # set direction
        self.__PI.set_PWM_dutycycle(self.__STEP_PIN, 128)           # start rotation
        sleep(SLEEP_TIMER)
        self.__PI.set_PWM_dutycycle(self.__STEP_PIN, 0)             # stop rotation

    def close(self) -> None:
        self.__PI.stop()

class Controller:
    __current_file: int = 0
    __current_rank: int = 0

    def __init__(self):
        self.__file_motor = StepperMotor(20, 21)
        self.__rank_motor = StepperMotor(5, 6)
        self.__magnet = Magnet(9)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__position_reset()
        self.__file_motor.close()
        self.__rank_motor.close()
        self.__magnet.close()

    def close(self) -> None:
        self.__exit__

    def __position_reset(self) -> None:
        '''This function will undo any stored movement.'''
        with ThreadPoolExecutor(max_workers = 2) as executor:
            executor.map(self.__file_motor.rotate, (-self.__current_file,))
            executor.map(self.__rank_motor.rotate, (-self.__current_rank,))

    def __get_rank_and_file_from_position(self, position: str) -> tuple:
        '''Maps a chess position to a tuple of two integers.
        E.g., "a1" to (1,1) and "b2" to (2,2) and "e8" to (5,8).'''
        return (FILE_MAP.get(position[0]), int(position[1]))

    def __position_file_and_rank(self, position: str) -> None:
        '''Takes in a chess position, e.g., "b1" and rotates the rank and file motors 
        to place the electromagnet under the given position.'''
        file, rank = self.__get_rank_and_file_from_position(position)
        file_rotations: int = (file - self.__current_file)
        rank_rotations: int = (rank - self.__current_rank)

        with ThreadPoolExecutor(max_workers = 2) as executor:
            executor.map(self.__file_motor.rotate, (file_rotations,))
            executor.map(self.__rank_motor.rotate, (rank_rotations,))

        self.__current_file = file
        self.__current_rank = rank

    def __grab(self) -> None:
        '''Grabs the chess piece.'''
        self.__magnet.activate()

    def __release(self) -> None:
        '''Releases the chess piece.'''
        self.__magnet.deactivate()

    def move(self, move: dict) -> None:
        '''Takes in a chess move as a dictionary, e.g., {"source": b1, "target": c3}.
        1. Places the electromagnet at the source position.
        2. Activates the electromagnet.
        3. Drags the piece to the target position.
        4. Drops it.
        5. Resets the position.'''
        self.__position_file_and_rank(move.get("source"))
        self.__grab()
        self.__position_file_and_rank(move.get("target"))
        self.__release()
        self.__position_reset()

if __name__ == "__main__":
    # for unit testing purposes
    move_to_perform: dict = {"source": "b1", "target": "c3"}

    with Controller() as controller:
        controller.move(move_to_perform)