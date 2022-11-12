from sys import argv

BOARD_STATE: dict[str, list[str]] = {
    "file": ["a", "b", "c", "d", "e", "f", "g", "h"],
    "rank": ["1", "2", "3", "4", "5", "6", "7", "8"]
}


def is_valid_move(request: dict[str, str]) -> bool:
    '''Checks move from/to input is [a-h] and rank is [1-8])'''
    move_from: dict[str, str] = {
        "file": request.get("fileFrom"),
        "rank": request.get("rankFrom")
    }

    move_to: dict[str, str] = {
        "file": request.get("fileTo"),
        "rank": request.get("rankTo")
    }

    return all([move_from.get(k) in v and move_to.get(k) in v
                for k, v in BOARD_STATE.items()])


if __name__ == "__main__":
    # for unit testing purposes
    print(is_valid_move({
        "fileFrom": argv[1],
        "rankFrom": argv[2],
        "fileTo": argv[3],
        "rankTo": argv[4]
    }))
