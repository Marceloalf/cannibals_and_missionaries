from status_class import *
from graph import *
from pygame_helpers import run


POSSIBLE_MOVES = [
    (0, 1),
    (0, 2),
    (1, 1),
    (1, 0),
    (2, 0),
]


def possibilities(status, priority_list, visited, graph):
    visited.append(status.representation())

    for movements in POSSIBLE_MOVES:
        new_status = move(status, *movements)

        if new_status and \
           new_status.is_valid() \
           and not status_already_verified(status, new_status, priority_list, visited, movements):

            new_status.add_adjacency({"node": status, "weight": movements})
            priority_list.append(new_status)
            graph.append_nodes(new_status)

            defining_objective_status(new_status, graph)


def defining_objective_status(status, graph):
    objective = {
            "right_border": [3, 3],
            "left_border": [0, 0],
            "boat": "right"
    }

    if status.representation() == objective:
        graph.objective = status


def status_already_verified(status, new_status, priority_list, visited, movement):
    if new_status.representation() in visited:
        new_status.add_adjacency({"node": status, "weight": movement})
        return True
    else:
        for priority in priority_list:
            if new_status.representation() == priority.representation():
                new_status.add_adjacency({"node": status, "weight": movement})
                return True


def get_solution_path():
    visited = []
    priority_list = [Status()]

    graph = Graph()
    graph.append_nodes(priority_list[0])

    graph.init = priority_list[0]

    while priority_list:
        priority = priority_list.pop(0)
        possibilities(priority, priority_list, visited, graph)

    return graph.generate_path([graph.objective])


def main():
    paths = list(get_solution_path())[0][::-1]
    run(paths)


if __name__ == '__main__':
    main()
