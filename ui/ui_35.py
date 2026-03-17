import pygame
from ui.base_ui import BaseUI, Button
from ui.constants import CELL_SIZE, BUTTON_HEIGHT, PANEL_WIDTH
import config
from core.grid import Grid
from core.player import Player

class UI_35(BaseUI):
    # Intermediate UI for grade 3-5
    
    def __init__(self, simulation):
        from core.grid import Grid
        simulation.grid = Grid(15, 15)
        self.grid = simulation.grid

        from core.player import Player
        simulation.players = [
            Player(1, 0, 0),
            Player(2, self.grid.width - 1, self.grid.height - 1)
        ]

        from core.random_walk import RandomWalkProtocol
        simulation.protocol = RandomWalkProtocol()

        super().__init__(simulation)

        self.placement_mode = False

        self._create_35_buttons()

    def _create_35_buttons(self):
        # Create buttons specific to the Grades 3–5 UI
        from ui.base_ui import Button  # avoid circular import

        panel_x = self.grid.width * CELL_SIZE + 20
        y = self.next_button_y

        # Choose movement protocol
        self.protocol_button = Button(
            (panel_x, y, PANEL_WIDTH - 40, BUTTON_HEIGHT),
            "Switch Protocol",
            self.switch_protocol,
            self.font
        )
        self.buttons.append(self.protocol_button)
        y += BUTTON_HEIGHT + 10
        self.next_button_y = y + 20

        # Add any other 3–5 specific buttons here
        # Example: Show path toggle
        self.show_path_button = Button(
            (panel_x, y, PANEL_WIDTH - 40, BUTTON_HEIGHT),
            "Toggle Path",
            self.toggle_path,
            self.font
        )
        self.buttons.append(self.show_path_button)
        self.next_button_y = y + 20

    def switch_protocol(self):
        # Toggle between Random Walk and Wall Hugging protocols
        from core.random_walk import RandomWalkProtocol
        from core.wall_hugging import WallHuggingProtocol

        if isinstance(self.simulation.protocol, RandomWalkProtocol):
            self.simulation.protocol = WallHuggingProtocol()
            self.protocol_button.text = "Protocol: Wall Hugging"
        else:
            self.simulation.protocol = RandomWalkProtocol()
            self.protocol_button.text = "Protocol: Random Walk"

    def cycle_grid(self):
        if self.simulation.is_running:
            return
        self.grid_preset_index = (self.grid_preset_index + 1) % len(config.GRID_PRESETS)
        self._reset_players_for_grid()

    def toggle_placement(self):
        if not self.simulation.is_running:
            self.placement_mode = not self.placement_mode
            self.place_button.text = f"Placement: {'ON' if self.placement_mode else 'OFF'}"

    def toggle_path(self):
        # Toggle whether player paths are drawn on the grid
        self.simulation.show_path = not getattr(self.simulation, "show_path", False)

        if self.simulation.show_path:
            self.show_path_button.text = "Hide Path"
        else:
            self.show_path_button.text = "Show Path"

    def _reset_players_for_grid(self):
        width, height = config.GRID_PRESETS[self.grid_preset_index]
        self.simulation.grid = Grid(width, height)
        self.grid = self.simulation.grid

        self.simulation.players = []
        for i in range(self.num_players):
            self.simulation.players.append(Player(i + 1, 0, 0))
        self.simulation.reset()

        width_px = self.grid.width * CELL_SIZE + PANEL_WIDTH
        height_px = max(self.grid.height * CELL_SIZE, BUTTON_HEIGHT * 2 + 20)
        self.screen = pygame.display.set_mode((width_px,height_px))

    def random_place_players(self):
        if self.simulation.is_running:
            return
        import random
        used = set()
        for p in self.simulation.players:
            while True:
                x = random.randint(0, self.grid.width - 1)
                y = random.randint(0, self.grid.height - 1)
                if (x, y) not in used:
                    used.add((x, y))
                    p.x, p.y = x, y
                    break

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.stats_manager:
                    self.stats_manager.export_to_csv("run_stats.csv")
                pygame.quit()
                raise SystemExit

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.placement_mode and not self.simulation.is_running:
                    x, y = event.pos
                    grid_x = x // CELL_SIZE
                    grid_y = y // CELL_SIZE
                    if 0 <= grid_x < self.grid.width and 0 <= grid_y < self.grid.height:
                        # Place players sequentially
                        unplaced = [p for p in self.simulation.players if (p.x, p.y) == (0, 0)]
                        if unplaced:
                            unplaced[0].x, unplaced[0].y = grid_x, grid_y
                        else: 
                            self.simulation.players[-1].x, self.simulation.players[-1].y = grid_x, grid_y

            for b in self.buttons:
                b.handle_event(event)

    def draw_mode_indicator(self):
        text = f"Placement Mode: {'ON' if self.placement_mode else 'OFF'}"
        color = (0, 150, 0) if self.placement_mode else (120, 120, 120)
        surf = self.font.render(text, True, color)
        self.screen.blit(surf, (10, 140))

    def draw(self):
        super().draw()
        self.draw_mode_indicator()
