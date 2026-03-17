import random
from core.stats import StatsManager
from core.random_walk import RandomWalkProtocol

class SimulationEngine:
    # Controls the simulation loop and movement logic

    def __init__(self):
        self.grid = None
        self.players = []
        self.protocol = None
        self.step_count = 0
        self.is_running = False
        self.stats_manager = StatsManager()
        self.ui = None

    def start(self):
        if self.grid is None or not self.players:
            return
        self.is_running = True

    def pause(self):
        self.is_paused = True

    def resume(self):
        self.is_paused = False

    def reset(self):
        self.step_count = 0
        for p in self.players:
            p.step_count = 0
            p.path = [(p.x, p.y)]
        self.is_running = False

    def update(self):
        if not self.is_running:
            return
        
        for p in self.players:
            p.move(self.grid)

        if self.players_met():
            self.is_running = False
        
        # Move each player
        for p in self.players:
            if self.protocol:
                dx, dy = self.protocol.get_next_move(p, self.grid)
            else:
                dx, dy = RandomWalkProtocol().get_next_move(p, self.grid)

            new_x = p.x + dx
            new_y = p.y + dy

            if self.grid.in_bounds(new_x, new_y):
                p.move_to(new_x, new_y)

        self.step_count += 1

        # Meeting detection
        if self.detect_meeting():
            self.is_running = False
            self.stats_manager.record_run(self.step_count)

            # Celebration for K-2
            if self.ui and hasattr(self.ui, "play_celebration"):
                self.ui.play_celebration()

    def players_met(self):
        if len(self.players) < 2:
            return False

        p1, p2 = self.players[0], self.players[1]
        return p1.x == p2.x and p1.y == p2.y

    def detect_meeting(self):
        positions = [(p.x, p.y) for p in self.players]
        return len(set(positions)) == 1
