from time import sleep
from concurrent.futures import ThreadPoolExecutor
from objects import StepperMotor, ElectroMagnet


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

class Controller:
    __scaling_factor: int = 7
    __current_file: int = 0
    __current_rank: int = 0

    def __init__(self):
        self.__FILE_MOTOR = StepperMotor(5, 6)
        self.__RANK_MOTOR = StepperMotor(20, 21)
        self.__MAGNET = ElectroMagnet(9)
        self.__set_motor_scale(self.__scaling_factor)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__FILE_MOTOR.close()
        self.__RANK_MOTOR.close()
        self.__MAGNET.close()

    def reset(self) -> None:
        '''Resets the gantry system position.'''
        MAX_ROTATIONS_FOR_BOARD = 57

        self.__set_motor_scale(1)

        with ThreadPoolExecutor(max_workers=2) as executor:
            executor.map(self.__FILE_MOTOR.rotate, (-MAX_ROTATIONS_FOR_BOARD,))
            executor.map(self.__RANK_MOTOR.rotate, (-MAX_ROTATIONS_FOR_BOARD,))

        sleep(1)

        with ThreadPoolExecutor(max_workers=2) as executor:
            executor.map(self.__FILE_MOTOR.rotate, (1,))
            executor.map(self.__RANK_MOTOR.rotate, (1,))
        
        sleep(1)

        self.__set_motor_scale(self.__scaling_factor)

    def __set_motor_scale(self, scaling_factor: float):
        '''Sets the scaling factor for the rank and file motors.'''
        for motor in [self.__FILE_MOTOR, self.__RANK_MOTOR]:
            motor.set_scale(scaling_factor)

    def __position_reset(self) -> None:
        '''This function will undo any stored movement.'''
        with ThreadPoolExecutor(max_workers=2) as executor:
            executor.map(self.__FILE_MOTOR.rotate, (-self.__current_file,))
            executor.map(self.__RANK_MOTOR.rotate, (-self.__current_rank,))
        sleep(1)

    def __to_cartesian_position(self, chess_position: str) -> tuple:
        '''Maps a chess position to a tuple of two integers (x, y).
        E.g., "a1" to (1,1) and "b2" to (2,2) and "e8" to (5,8).'''
        return (FILE_MAP.get(chess_position[0]), int(chess_position[1]))

    def __position_file_and_rank(self, position: str) -> None:
        '''Takes in a chess position, e.g., "b1" and rotates the rank and file motors 
        to place the electromagnet under the given position.'''
        FILE, RANK = self.__to_cartesian_position(position)
        FILE_ROTATIONS: int = (FILE - self.__current_file)
        RANK_ROTATIONS: int = (RANK - self.__current_rank)

        with ThreadPoolExecutor(max_workers=2) as executor:
            executor.map(self.__FILE_MOTOR.rotate, (FILE_ROTATIONS,))
            executor.map(self.__RANK_MOTOR.rotate, (RANK_ROTATIONS,))

        sleep(1)

        self.__current_file = FILE
        self.__current_rank = RANK

    def __grab(self) -> None:
        '''Grabs the chess piece.'''
        self.__MAGNET.activate()

    def __release(self) -> None:
        '''Releases the chess piece.'''
        self.__MAGNET.deactivate()

    def move(self, move: dict) -> None:
        '''Takes in a chess move as a dictionary, e.g., {"source": b1, "target": c3} and performs the move'''
        self.__position_file_and_rank(move.get("source"))
        self.__grab()
        self.__position_file_and_rank(move.get("target"))
        self.__release()
        self.__position_reset()


if __name__ == "__main__":
    # for unit testing purposes
    move_to_perform: dict = {"source": "c3", "target": "h8"}

    with Controller() as controller:
        controller.move(move_to_perform)