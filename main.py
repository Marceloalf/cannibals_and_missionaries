from status_class import *


POSSIBLE_MOVES = [
    (0, 1),
    (0, 2),
    (1, 1),
    (1, 0),
    (2, 0),
]


def possibilities(status):
    for movements in POSSIBLE_MOVES:
        s = move(status, *movements)


initial_status = Status()
possibilities(initial_status)

