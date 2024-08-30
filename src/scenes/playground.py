import pygame
import pygame_gui

from .scene import BaseScene


class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, groups: list[pygame.sprite.Group]):
        super().__init__(groups)

        self.image = pygame.Surface((50, 50))
        self.image.fill("red")
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        self.rect.x += 1


class Scene(BaseScene):
    def __init__(self, gui_manager: pygame_gui.UIManager = None):
        super().__init__()

        self.visible_sprites = pygame.sprite.Group()

        self.player = Player(100, 100, [self.visible_sprites])

    def run(self):
        self.visible_sprites.update()

        self.visible_sprites.draw(self.display_surface)
