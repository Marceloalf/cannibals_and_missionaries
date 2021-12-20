import pygame
from pygame.locals import *
from sys import exit
from status_class import *
from graph import *


POSSIBLE_MOVES = [
    (0, 1),
    (0, 2),
    (1, 1),
    (1, 0),
    (2, 0),
]

MISSIONARIES_COLOR = (140, 140, 200)
CANNIBALS_COLOR = (140, 0, 0)
BOAT_COLOR = (120, 64, 8)
BASE_RADIUS = 30
RIVER_COLOR = (0, 119, 190)
GRASS_COLOR = (86, 125, 70)

CAPTION = 'Missionarios e Canibais'

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720


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


def search_weight(from_, to_):
    for adjacency in to_.adjacency:
        if adjacency["node"].representation() == from_.representation():
            return adjacency["weight"]


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


def draw_left(screen, cannibals, missionaries):
    y = 80

    for cannibals_ in range(cannibals):
        pygame.draw.circle(screen, CANNIBALS_COLOR, (200, y), BASE_RADIUS)
        y += 100

    for missionaries_ in range(missionaries):
        pygame.draw.circle(screen, MISSIONARIES_COLOR, (200, y), BASE_RADIUS)
        y += 100


def draw_right(screen, cannibals, missionaries):
    y = 80

    for cannibals_ in range(cannibals):
        pygame.draw.circle(screen, CANNIBALS_COLOR, (1000, y), BASE_RADIUS)
        y += 100

    for missionaries_ in range(missionaries):
        pygame.draw.circle(screen, MISSIONARIES_COLOR, (1000, y), BASE_RADIUS)
        y += 100


def draw_boat(screen, position, weight):
    x = position + 50
    pygame.draw.rect(screen, BOAT_COLOR, (position, 600, 200, 50), border_radius=50)

    if weight:
        for cannibals_ in range(weight[0]):
            pygame.draw.circle(screen, CANNIBALS_COLOR, (x, 550), BASE_RADIUS)
            x += 100
        for missionaries_ in range(weight[1]):
            pygame.draw.circle(screen, MISSIONARIES_COLOR, (x, 550), BASE_RADIUS)
            x += 100


def boat_move(from_, boat_position, weight):
    missionaries_right = from_.border_right.missionaries
    cannibals_right = from_.border_right.cannibals

    missionaries_left = from_.border_left.missionaries
    cannibals_left = from_.border_left.cannibals

    if boat_position > 300 and from_.boat == "left":
        missionaries_left = (from_.border_left.missionaries - weight[1])
        cannibals_left = from_.border_left.cannibals - weight[0]

    elif boat_position < 900 and from_.boat == "right":
        missionaries_right = from_.border_right.missionaries - weight[1]
        cannibals_right = from_.border_right.cannibals - weight[0]

    right = (cannibals_right, missionaries_right)
    left = (cannibals_left, missionaries_left)

    return right, left


def updating_status(from_, boat_position, init):
    if from_.boat == "left" and boat_position == 750:
        return init + 1
    elif from_.boat == "right" and boat_position == 300:
        return init + 1
    else:
        return init


def updating_boat_position(from_, boat_position, speed):
    if from_.boat == "left":
        return boat_position + speed
    elif from_.boat == "right":
        return boat_position - speed


def main():
    paths = list(get_solution_path())[0][::-1]

    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(CAPTION)

    init = 0
    boat_position = 300

    final = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        if final:
            pygame.display.update()
            screen.fill(GRASS_COLOR)
            from_ = paths[-1]

            draw_left(screen, from_.border_left.cannibals, from_.border_left.missionaries)
            draw_right(screen, from_.border_right.cannibals, from_.border_right.missionaries)
            pygame.draw.rect(screen, RIVER_COLOR, (250, 0, 700, 1280), )

        if not final:
            from_ = paths[init]
            to_ = paths[init + 1]
            weight = search_weight(from_, to_)

            init = updating_status(from_, boat_position, init)
            boat_position = updating_boat_position(from_, boat_position, 0.5)
            right, left = boat_move(from_, boat_position, weight)

            screen.fill(GRASS_COLOR)

            pygame.draw.rect(screen, RIVER_COLOR, (250, 0, 700, 1280),)
            draw_left(screen, *left)
            draw_right(screen, *right)

            draw_boat(screen, boat_position, weight)

            if init + 1 == len(paths):
                final = True

        pygame.display.update()


if __name__ == '__main__':
    main()
