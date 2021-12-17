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

        if new_status and \
           new_status.is_valid() \
           and not status_already_verified(status, new_status, priority_list, visited, movements):

            priority_list.append(new_status)


def status_already_verified(status, new_status, priority_list, visited, movement):
    if new_status.representation() in visited:
        status.add_adjacency({"node": new_status, "weight": movement})
        return True
    else:
        for priority in priority_list:
            if new_status.representation() == priority.representation():
                status.add_adjacency({"node": new_status, "weight": movement})
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
