import pygame


class DebugOverlay:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 36)

        self.stack = []

    def append(self, text: str, color: str = "white"):
        debug_surface = self.font.render(text, True, color)
        self.stack.append(debug_surface)

    def update(self):
        self.stack.clear()

    def draw(self):
        for index, surface in enumerate(self.stack):
            self.display_surface.blit(surface, (10, 10 + index * 30))
