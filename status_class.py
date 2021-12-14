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

    def representation(self):
        """
        It will help later on the priority list of status
        """
        return {
            "cannibals": self.cannibals,
            "missionaries": self.missionaries
        }

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


class Status:
    def __init__(self, cannibals_left=3, missionaries_left=3, boat="left"):
        """
        The standard status begins with everyone and the boat on the left border.
        """
        self.border_left = Border(cannibals_left, missionaries_left)
        self.border_right = Border(3 - cannibals_left, 3 - missionaries_left)
        self.boat = boat


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

    if status.boat == "right":
        border_left = status.border_left.arrive(cannibals, missionaries)

        return Status(border_left["cannibals"], border_left["missionaries"], "left")

    elif status.boat == "left":
        border_left = status.border_left.leave(cannibals, missionaries)

        return Status(border_left["cannibals"], border_left["missionaries"], "right")


def cant_move(cannibals, missionaries):
    """
    If the boat have more than 2 people or have no people at all, it can't move
    """
    return (cannibals + missionaries > 2) or (cannibals + missionaries < 1)
