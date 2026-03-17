import pygame
from ui.constants import PANEL_WIDTH, BUTTON_HEIGHT

class GradeSelectUI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 36)
        self.buttons = []
        self.create_buttons()

    def create_buttons(self):
        w, h = self.screen.get_size()
        x = w // 2 - 100
        y = h // 2 - 100

        from ui.base_ui import Button
        self.buttons = [
            Button((x, y, 200, 50), "K-2", lambda: "K2", self.font),
            Button((x, y + 70, 200, 50), "3-5", lambda: "35", self.font),
            Button((x, y + 140, 200, 50), "6-8", lambda: "68", self.font),
        ]

    def run(self):
        import pygame
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                
                for b in self.buttons:
                    result = b.handle_event(event)
                    if result:
                        return result # return grade level string
            self.screen.fill((255, 255, 255)) 
            title = self.font.render("Select Grade Level", True, (0, 0, 0))
            self.screen.blit(title, (self.screen.get_width()//2 - title.get_width()//2, 80))

            for b in self.buttons:
                b.draw(self.screen)

            pygame.display.flip()
            clock.tick(30)
            