import random
from core.movement_protocol import MovementProtocol

class RandomWalkProtocol(MovementProtocol):
    # Players move randomly to any valid neighboring cell

    def get_next_move(self, player, grid):
        neighbors = grid.get_neighbors(player.x, player.y)
        return random.choice(neighbors)