class Grid:
    # Represents the 2D forest environemnt

    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height

    def in_bounds(self, x, y):
        # Return true if (x, y) is inside the grid
        return 0 <= x < self.width and 0 <= y < self.height
    
    def get_neighbors(self, x, y):
        # Return valid adjacent positions
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        neighbors = []

        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if self.in_bounds(nx, ny):
                neighbors.append((nx, ny))

        return neighbors

