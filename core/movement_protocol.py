from abc import ABC, abstractmethod

class MovementProtocol(ABC):
    # Abstract base class for all movement strategies

    @abstractmethod
    def get_next_move(self, player, grid):
        # Return the next (x, y) position for the player
        pass
    