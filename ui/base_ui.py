import pygame
from pygame import Rect

from ui.constants import CELL_SIZE, BUTTON_HEIGHT, PANEL_WIDTH

class Button:
    def __init__(self, rect, text, callback, font):
        self.rect = Rect(rect)
        self.text = text
        self.callback = callback
        self.font = font

    def draw(self, surface):
        pygame.draw.rect(surface, (220, 220, 220), self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 1)
        label = self.font.render(self.text, True, (0, 0, 0))
        surface.blit(label, label.get_rect(center=self.rect.center))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return self.callback()

class BaseUI:
    # Shared UI logic for all grade levels

    def __init__(self, simulation):
        self.simulation = simulation
        self.grid = simulation.grid
        self.players = simulation.players
        self.stats_manager = simulation.stats_manager
       
        # Window setup
        width = self.grid.width * CELL_SIZE + PANEL_WIDTH
        height = max(self.grid.height * CELL_SIZE, 600)
        self.screen = pygame.display.set_mode((width, height))

        # Shared UI resources
        self.font = pygame.font.SysFont(None, 28)
        self.buttons = []

        self.clock = pygame.time.Clock()

        self._create_default_buttons()

    def _create_default_buttons(self):
        from ui.base_ui import Button  # avoid circular import

        panel_x = self.grid.width * CELL_SIZE + 20
        y = 20

        # Pause / Resume
        self.pause_button = Button(
            (panel_x, y, PANEL_WIDTH - 40, BUTTON_HEIGHT),
            "Pause",
            self.toggle_pause,
            self.font
        )
        self.buttons.append(self.pause_button)
        y += BUTTON_HEIGHT + 10

        # Reset
        self.reset_button = Button(
            (panel_x, y, PANEL_WIDTH - 40, BUTTON_HEIGHT),
            "Reset",
            self.reset_simulation,
            self.font
        )
        self.buttons.append(self.reset_button)
        y += BUTTON_HEIGHT + 10

        # Run Again
        self.run_again_button = Button(
            (panel_x, y, PANEL_WIDTH - 40, BUTTON_HEIGHT),
            "Run Again",
            self.run_again,
            self.font
        )
        self.buttons.append(self.run_again_button)

        self.next_button_y = y + BUTTON_HEIGHT + 20

    def _create_buttons(self):
        panel_x = self.grid.width * CELL_SIZE + 20
        y = 20

        # Pause/Resume
        self.pause_button = Button(
            (panel_x, y, PANEL_WIDTH - 40, BUTTON_HEIGHT),
            "Pause",
            self.toggle_pause,
            self.font
        )
        self.buttons.append(self.pause_button)
        y += BUTTON_HEIGHT + 10

        # Reset
        self.reset_button = Button(
            (panel_x, y, PANEL_WIDTH - 40, BUTTON_HEIGHT),
            "Reset",
            self.reset_simulation,
            self.font
        )
        self.buttons.append(self.reset_button)
        y += BUTTON_HEIGHT + 20

        self.next_button_y = y

        # Save the next available Y position for subclasses
        self.next_button_y = y + BUTTON_HEIGHT + 20

    def toggle_pause(self):
        if self.simulation.is_running:
            self.simulation.is_running = False
            self.pause_button.text = "Resume"
        else:
            self.simulation.is_running = True
            self.pause_button.text = "Pause"

    def reset_simulation(self):
        self.simulation.reset()

    def run_again(self):
        self.simulation.reset()
        self.simulation.start()

    def draw_grid(self):
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                rect = Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                color = (230, 255, 230) if (x + y) % 2 == 0 else (210, 240, 210)
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (180, 180, 180), rect, 1)

    def draw_players(self):
        for p in self.simulation.players:
            if len(p.path) > 1:
                points = [(x * CELL_SIZE + CELL_SIZE // 2,
                           y * CELL_SIZE + CELL_SIZE // 2) for (x, y) in p.path]
                pygame.draw.lines(self.screen, (150, 150, 255), False, points, 2)

        for p in self.simulation.players:
            rect = Rect(p.x * CELL_SIZE + 5, p.y * CELL_SIZE + 5,
                        CELL_SIZE - 10, CELL_SIZE - 10)
            pygame.draw.rect(self.screen, (255, 100, 100), rect)

    def draw_stats_panel(self):
        panel_x = self.grid.width * CELL_SIZE
        rect = Rect(panel_x, 0, PANEL_WIDTH, self.screen.get_height())
        pygame.draw.rect(self.screen, (245, 245, 245), rect)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)

        y = self.next_button_y # Start stats BELOW buttons
        title = self.font.render("Stats", True, (0, 0, 0))
        self.screen.blit(title, (panel_x + 20, y))
        y += 30

        if self.stats_manager:
            summary = self.stats_manager.get_summary()
            if summary:
                for label, key in [("Runs", "count"), ("Min", "min"),
                                   ("Max", "max"), ("Avg", "avg")]:
                    text = f"{label}: {summary[key]: .2f}" if isinstance(summary[key], float) else f"{label}: {summary[key]}"
                    surf = self.font.render(text, True, (0, 0, 0))
                    self.screen.blit(surf, (panel_x + 20, y))
                    y += 25
            else:
                msg = self.font.render("No runs yet", True, (100, 100, 100))
                self.screen.blit(msg, (panel_x + 20, y))

    def draw_buttons(self):
        for b in self.buttons:
            b.draw(self.screen)

    def draw_tooltip(self):
            mouse_pos = pygame.mouse.get_pos()
            for b in self.buttons:
                if b.rect.collidepoint(mouse_pos):
                    tooltip = self.font.render(b.text, True, (255, 255, 255))
                    bg_rect = tooltip.get_rect()
                    bg_rect.topleft = (mouse_pos[0] + 12, mouse_pos[1] + 12)
                    pygame.draw.rect(self.screen, (0, 0, 0), bg_rect.inflate(6, 6))
                    self.screen.blit(tooltip, bg_rect)
                    return

    def draw_instructions(self):
        lines = [
            "Controls:",
            "G = Change Grid Size (3-5, 6-8)",
            "P = Toggle Placement Mode (3-5)",
            "Click = Place Players (3-5)",
            "Buttons > Pause, Reset, Protocol, Batch, Graph"
        ]

        x = 10
        y = 10
        for line in lines:
            surf = self.font.render(line, True, (0, 0, 0))
            self.screen.blit(surf, (x, y))
            y += 22

    def draw_highlight_cell(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        grid_x = mouse_x // CELL_SIZE
        grid_y = mouse_y // CELL_SIZE

        if 0 <= grid_x < self.grid.width and 0 <= grid_y < self.grid.height:
            rect = Rect(grid_x * CELL_SIZE, grid_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, (255, 255, 0, 80), rect, 3)

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.draw_instructions()
        self.draw_grid()
        self.draw_highlight_cell()
        self.draw_players()
        self.draw_stats_panel()
        self.draw_buttons()
        self.draw_tooltip()

    def handle_event(self, event):
        pass

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Handle button clicks
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        button.handle_event(event)

                # Let subclasses handle extra events
                self.handle_event(event)

            if self.simulation.is_running:
                self.simulation.update()

            self.draw()
            pygame.display.flip()
            self.clock.tick(5)
