from sys import argv

from controllers import BOARD_STATE


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


if __name__ == "__main__":
    # for unit testing purposes
    print(is_valid_move({
        "fileFrom": argv[1],
        "rankFrom": argv[2],
        "fileTo": argv[3],
        "rankTo": argv[4]
    }))
