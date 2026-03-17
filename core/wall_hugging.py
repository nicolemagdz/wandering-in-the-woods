from core.movement_protocol import MovementProtocol

class WallHuggingProtocol(MovementProtocol):
    """
    Players move clockwise along the boundary
    If not on boundary, they move toward the nearest wall
    """

    def get_next_move(self, player, grid):
        x, y = player.x, player.y

        # If on boundary, follow clockwise pattern
        if y == 0 and x < grid.width - 1:
            return (x + 1, y)
        if x == grid.width - 1 and y < grid.height - 1:
            return (x, y + 1)
        if y == grid.height - 1 and x > 0:
            return (x - 1, y)
        if x == 0 and y > 0:
            return (x, y - 1)
        
        # If not on boundary, move upward until reaching boundary
        return (x, y - 1) if y > 0 else (x, y)