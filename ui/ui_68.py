import pygame
from ui.base_ui import BaseUI, Button
from ui.constants import CELL_SIZE, BUTTON_HEIGHT, PANEL_WIDTH
import config
from core.grid import Grid
from core.player import Player
from core.random_walk import RandomWalkProtocol
from core.wall_hugging import WallHuggingProtocol
from core.graphs import show_steps_line_chart

PROTOCOLS = [
    ("Random", RandomWalkProtocol),
    ("Wall", WallHuggingProtocol),
]

class UI_68(BaseUI):
    # Advanced UI for grades 6-8
    
    def __init__(self, simulation):
        # 1. Create grid for Grades 6–8
        from core.grid import Grid
        simulation.grid = Grid(20, 20)   # or whatever size you want
        self.grid = simulation.grid

        # 2. Create players
        from core.player import Player
        simulation.players = [
            Player(1, 0, 0),
            Player(2, self.grid.width - 1, self.grid.height - 1)
        ]

        # 3. Set protocol (6–8 usually uses a more advanced one)
        from core.random_walk import RandomWalkProtocol
        simulation.protocol = RandomWalkProtocol()

        # 4. Base UI setup (now safe)
        super().__init__(simulation)

        # 5. UI‑specific state
        self.placement_mode = False
        self.show_path = False

        # 6. Create 6–8 specific buttons
        self._create_68_buttons()

    def _create_68_buttons(self):
        # Create buttons specific to the Grades 6–8 UI
        from ui.base_ui import Button  # avoid circular import

        panel_x = self.grid.width * CELL_SIZE + 20
        y = self.next_button_y

        # Toggle placement mode
        self.placement_button = Button(
            (panel_x, y, PANEL_WIDTH - 40, BUTTON_HEIGHT),
            "Placement: OFF",
            self.toggle_placement_mode,
            self.font
        )
        self.buttons.append(self.placement_button)
        y += BUTTON_HEIGHT + 10
        self.next_button_y = y + 20

        # Toggle path visibility
        self.path_button = Button(
            (panel_x, y, PANEL_WIDTH - 40, BUTTON_HEIGHT),
            "Show Path",
            self.toggle_path,
            self.font
        )
        self.buttons.append(self.path_button)
        y += BUTTON_HEIGHT + 10

        # Switch protocol
        self.protocol_button = Button(
            (panel_x, y, PANEL_WIDTH - 40, BUTTON_HEIGHT),
            "Protocol: Random Walk",
            self.switch_protocol,
            self.font
        )
        self.buttons.append(self.protocol_button)
        self.next_button_y = y + 20

    def toggle_placement_mode(self):
        # Toggle whether the user is placing players on the grid
        self.placement_mode = not self.placement_mode

        if self.placement_mode:
            self.placement_button.text = "Placement: ON"
        else:
            self.placement_button.text = "Placement: OFF"

    def toggle_path(self):
        # Toggle whether player paths are drawn on the grid
        self.show_path = not self.show_path

        if self.show_path:
            self.path_button.text = "Hide Path"
        else:
            self.path_button.text = "Show Path"

    def _create_advanced_buttons(self):
        x = self.grid.width * CELL_SIZE + 20
        y = self.next_button_y

        # Protocol menu
        self.protocol_button = Button(
            (x, y, 160, 40),
            "Protocol: Random",
            self.cycle_protocol,
            self.font
        )
        self.buttons.append(self.protocol_button)
        y += 50

        # Trial count selector
        self.trials_button = Button(
            (x, y, 160, 40),
            f"Trials: {self.batch_trials}",
            self.cycle_trials,
            self.font
        )
        self.buttons.append(self.trials_button)
        y += 50

        # Run batch
        self.batch_button = Button(
            (x, y, 160, 40),
            "Run Batch",
            self.run_batch_trials,
            self.font
        )
        self.buttons.append(self.batch_button)
        y += 50

        # Show graph
        self.graph_button = Button(
            (x, y, 160, 40),
            "Show Graph",
            self.show_graph,
            self.font
        )
        self.buttons.append(self.graph_button)
        y += 50

        # Data table
        self.table_button = Button(
            (x, y, 160, 40),
            "Show Table",
            self.show_table,
            self.font
        )
        self.buttons.append(self.table_button)
        y += 50

        # Protocol preview
        self.preview_button = Button(
            (x, y, 160, 40),
            "Preview Protocol",
            self.preview_protocol,
            self.font
        )
        self.buttons.append(self.preview_button)
        y += 50

        self.next_button_y = y + 10
    
    def _reset_for_current_grid(self):
        width, height = config.GRID_PRESETS[self.grid_preset_index]
        self.simulation.grid = Grid(width, height)
        self.grid = self.simulation.grid

        self.simulation.players = [
            Player(1, 0, 0),
            Player(2, self.grid.width - 1, self.grid.height - 1),
        ]
        self.simulation.reset()

        width_px = self.grid.width * CELL_SIZE + PANEL_WIDTH
        height_px = max(self.grid.height * CELL_SIZE, BUTTON_HEIGHT * 2 + 20)
        self.screen = pygame.display.set_mode((width_px, height_px))

    def cycle_protocol(self):
        self.protocol_index = (self.protocol_index + 1) % len(PROTOCOLS)
        name, cls = PROTOCOLS[self.protocol_index]
        self.simulation.protocol = cls()
        self.protocol_button.text = f"Protocol: {name}"

    def cycle_trials(self):
        self.batch_trials += 5
        if self.batch_trials > 50:
            self.batch_trials = 5
        self.trials_button.text = f"Trials: {self.batch_trials}"

    def run_batch_trials(self):
        # Run N trials automatically, no UI animation
        for _ in range(self.batch_trials):
            self.simulation.reset()
            self.simulation.start()
            while self.simulation.is_running:
                self.simulation.update()
        # After batch, stop simulation and redraw once
        self.simulation.is_running = False

    def show_graph(self):
        if self.stats_manager:
            show_steps_line_chart(self.stats_manager)

    def show_table(self):
        if not self.stats_manager or not self.stats_manager.run_history:
            return
        
        rows = self.stats_manager.run_history
        width, height = 400, 300
        table_screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Run Data Table")
        
        font = pygame.font.SysFont(None, 24)
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            table_screen.fill((255, 255, 255))
            y = 20
            header = font.render("Run   Steps", True, (0, 0, 0))
            table_screen.blit(header, (20, y))
            y += 30

            for i, r in enumerate(rows, start=1):
                line = font.render(f"{i:3d} {r['steps']}", True, (0, 0, 0))
                table_screen.blit(line, (20, y))
                y += 24
                if y > height - 30:
                    break

            pygame.display.flip()
            clock.tick(30)
        
        # Restore main window
        width_px = self.grid.width * CELL_SIZE + PANEL_WIDTH
        height_px = max(self.grid.height * CELL_SIZE, BUTTON_HEIGHT * 2 + 20)
        self.screen = pygame.display.set_mode((width_px, height_px))
        pygame.display.set_caption("Wandering in the Woods")

    def preview_protocol(self):
        demo_steps = 15
        self.simulation.reset()
        self.simulation.start()
        for _ in range(demo_steps):
            if not self.simulation.is_running:
                break
            self.simulation.update()
            self.draw()
            pygame.display.flip()
            pygame.time.delay(150)
        self.simulation.is_running = False

    def switch_protocol(self):
        #Toggle between Random Walk and Wall Hugging protocols
        from core.random_walk import RandomWalkProtocol
        from core.wall_hugging import WallHuggingProtocol

        if isinstance(self.simulation.protocol, RandomWalkProtocol):
            self.simulation.protocol = WallHuggingProtocol()
            self.protocol_button.text = "Protocol: Wall Hugging"
        else:
            self.simulation.protocol = RandomWalkProtocol()
            self.protocol_button.text = "Protocol: Random Walk"


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.stats_manager:
                    self.stats_manager.export_to_csv("run_stats.csv")
                pygame.quit()
                raise SystemExit
            
            if event.type == pygame.KEYDOWN:
                # Cycle grid presets with G
                if event.key == pygame.K_g and not self.simulation.is_running:
                    self.grid_preset_index = (self.grid_preset_index + 1) % len(config.GRID_PRESETS)
                    self._reset_for_current_grid()

            for b in self.buttons:
                b.handle_event(event)

