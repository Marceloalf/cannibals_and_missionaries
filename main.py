from status_class import *


POSSIBLE_MOVES = [
    (0, 1),
    (0, 2),
    (1, 1),
    (1, 0),
    (2, 0),
]


def possibilities(status, priority_list, visited):
    visited.append(status.representation())

    for movements in POSSIBLE_MOVES:
        new_status = move(status, *movements)

        if new_status and new_status.is_valid() and not invalid_status(new_status, priority_list, visited):
            priority_list.append(new_status)


def invalid_status(status, priority_list, visited):
    if not status:
        return True

    elif status.representation() in visited:
        return True

    else:
        for priority in priority_list:
            if status.representation() == priority.representation():
                return True


def main():
    visited = []
    priority_list = [Status()]

    while priority_list:
        priority = priority_list.pop(0)
        print(priority)
        print()
        possibilities(priority, priority_list, visited)


if __name__ == '__main__':
    main()
