from sys import argv

BOARD_STATE: dict[str, list[str]] = {
    "file": ["a", "b", "c", "d", "e", "f", "g", "h"],
    "rank": ["1", "2", "3", "4", "5", "6", "7", "8"]
}


def is_valid_move(form: dict[str, str]) -> bool:
    move_from: dict[str, str] = {
        "file": form.get("fileFrom"),
        "rank": form.get("rankFrom")
    }

    move_to: dict[str, str] = {
        "file": form.get("fileTo"),
        "rank": form.get("rankTo")
    }

    return all([move_from.get(k) in v and move_to.get(k) in v
                for k, v in BOARD_STATE.items()])


def get_from_position(form: dict[str, str]) -> tuple:
    return (
        form.get("fileFrom"),
        form.get("rankFrom")
    )


def get_to_position(form: dict[str, str]) -> tuple:
    return (
        form.get("fileTo"),
        form.get("rankTo")
    )


if __name__ == "__main__":
    # for unit testing purposes
    print(is_valid_move({
        "fileFrom": argv[1],
        "rankFrom": argv[2],
        "fileTo": argv[3],
        "rankTo": argv[4]
    }))
