class Border:
    def __init__(self, cannibals=0, missionaries=0):
        """
        Defines the amount of people in this specific border
        """
        self.cannibals = cannibals
        self.missionaries = missionaries

    def __repr__(self):
        # Helps the debug
        return f"Canibais: {self.cannibals}, missionários: {self.missionaries}"

    def leave(self, cannibals, missionaries):
        return {
            "cannibals": self.cannibals - cannibals,
            "missionaries": self.missionaries - missionaries
        }

    def arrive(self, cannibals, missionaries):
        return {
            "cannibals": self.cannibals + cannibals,
            "missionaries": self.missionaries + missionaries
        }

    def is_valid(self):
        """
        Verify if the border is valid
        :return: the only case forbidden is when cannibals > (missionaries != 0)
        """
        if self.cannibals == 0 or self.missionaries == 0:
            return True
        elif self.cannibals > self.missionaries:
            return False
        else:
            return True


class Status:
    def __init__(self, cannibals_left=3, missionaries_left=3, boat="left"):
        """
        The standard status begins with everyone and the boat on the left border.
        """

        # Border information
        self.border_left = Border(cannibals_left, missionaries_left)
        self.border_right = Border(3 - cannibals_left, 3 - missionaries_left)
        self.boat = boat

        # Graph information
        self.adjacency = []
        self.visited = False

    def representation(self):
        return {
            "right_border": [self.border_right.cannibals, self.border_right.missionaries],
            "left_border": [self.border_left.cannibals, self.border_left.missionaries],
            "boat": self.boat
        }

    def is_valid(self):
        """
        Verify if both borders in this status are valid
        :return: True if both are valid
        """
        return self.border_right.is_valid() and self.border_left.is_valid()

    def add_adjacency(self, edge):
        if edge not in self.adjacency:
            self.adjacency.append(edge)

    def __repr__(self):
        return f"(right_border: {self.border_right} | left_border: {self.border_left} | boat: {self.boat})"


def move(status, cannibals, missionaries):
    """
    Defines the amount of people who will move across borders
    :param status: the previous status of each border and the boat
    :param cannibals: the amount of cannibals moving
    :param missionaries: the amount of missionaries moving
    :return: a new status after all people move
    """
    if cant_move(cannibals, missionaries):
        return

    if status.boat == "right" and not not_enough_people(status, status.boat, cannibals, missionaries):
        border_left = status.border_left.arrive(cannibals, missionaries)

        return Status(border_left["cannibals"], border_left["missionaries"], "left")

    elif status.boat == "left" and not not_enough_people(status, status.boat, cannibals, missionaries):
        border_left = status.border_left.leave(cannibals, missionaries)

        return Status(border_left["cannibals"], border_left["missionaries"], "right")


def cant_move(cannibals, missionaries):
    """
    If the boat have more than 2 people or have no people at all, it can't move
    """
    return (cannibals + missionaries > 2) or (cannibals + missionaries < 1)


def not_enough_people(status, border, cannibals, missionaries):
    if border == "right":
        return status.border_right.cannibals < cannibals or status.border_right.missionaries < missionaries

    elif border == "left":
        return status.border_left.cannibals < cannibals or status.border_left.missionaries < missionaries
