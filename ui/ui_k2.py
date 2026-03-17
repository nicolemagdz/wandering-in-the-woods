import pygame
import random

from ui.base_ui import BaseUI, Button
from ui.constants import CELL_SIZE, BUTTON_HEIGHT, PANEL_WIDTH


class UI_K2(BaseUI):
    # Simplified UI for early elementary students (K–2).
    
    def __init__(self, simulation):
        self.has_started = False
        self.celebrating = False

        # Small grid for young learners
        from core.grid import Grid
        from core.player import Player

        simulation.grid = Grid(10, 10)
        self.grid = simulation.grid

        # Two players in opposite corners
        simulation.players = [
            Player(1, 0, 0),
            Player(2, self.grid.width - 1, self.grid.height - 1),
        ]

        super().__init__(simulation)

        self._create_k2_buttons()

    # Buttons
    def _create_k2_buttons(self):
        self.buttons = []

        panel_x = self.grid.width * CELL_SIZE + 20
        y = 20

        # Start button
        self.start_button = Button(
            (panel_x, y, PANEL_WIDTH - 40, BUTTON_HEIGHT),
            "Start",
            self.start_simulation,
            self.font,
        )
        self.buttons.append(self.start_button)
        y += BUTTON_HEIGHT + 10

        # Run Again button
        self.run_again_button = Button(
            (panel_x, y, PANEL_WIDTH - 40, BUTTON_HEIGHT),
            "Run Again",
            self.run_again,
            self.font,
        )
        self.buttons.append(self.run_again_button)
        y += BUTTON_HEIGHT + 10

        self.next_button_y = y + 20

    # Simulation control
    def start_simulation(self):
        self.simulation.reset()
        self.simulation.is_running = True
        self.has_started = True
        self.celebrating = False

    def run_again(self):
        self.start_simulation()

    # Meeting detection
    def players_met(self):
        p1, p2 = self.simulation.players
        return p1.x == p2.x and p1.y == p2.y

    # Celebration animation
    def play_celebration(self):
        self.celebrating = True

        for _ in range(20):
            self.screen.fill((255, 255, 255))

            # Confetti
            for _ in range(80):
                x = random.randint(0, self.screen.get_width())
                y = random.randint(0, self.screen.get_height())
                color = random.choice([
                    (255, 0, 0), (0, 255, 0), (0, 0, 255),
                    (255, 255, 0), (255, 0, 255), (0, 255, 255)
                ])
                pygame.draw.circle(self.screen, color, (x, y), 4)

            # Message
            msg = self.font.render("They Met!", True, (0, 0, 0))
            self.screen.blit(
                msg,
                (self.screen.get_width() // 2 - msg.get_width() // 2, 40),
            )

            pygame.display.flip()
            pygame.time.delay(80)

        self.celebrating = False
        self.has_started = False

    # Drawing
    def draw_players(self):
        # Friendly circles for K–2
        for p in self.simulation.players:
            cx = p.x * CELL_SIZE + CELL_SIZE // 2
            cy = p.y * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.circle(
                self.screen,
                (255, 100, 100),
                (cx, cy),
                CELL_SIZE // 2 - 6,
            )

    def draw(self):
        # If simulation stopped because players met > celebrate
        if self.has_started and not self.simulation.is_running and not self.celebrating:
            self.play_celebration()
            return

        # Normal drawing
        self.screen.fill((255, 255, 255))
        self.draw_instructions()
        self.draw_grid()
        self.draw_players()
        self.draw_stats_panel()
        self.draw_buttons()
        self.draw_tooltip()
