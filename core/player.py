import random

class Player:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

    def move(self, grid):
        dx, dy = random.choice([
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
            (0, 0),  # sometimes stay still
        ])

        new_x = self.x + dx
        new_y = self.y + dy

        new_x = max(0, min(grid.width - 1, new_x))
        new_y = max(0, min(grid.height - 1, new_y))

        self.x = new_x
        self.y = new_y

    def move_to(self, x, y):
        self.x = x
        self.y = y
