import random

import pygame
import pygame_gui as gui

from src.components.scene import BaseScene
from src.player import Player, debug_player


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)

        self.image = pygame.Surface((50, 50))
        self.image.fill("red")
        self.rect = self.image.get_rect(topleft=pos)


class Scene(BaseScene):
    def __init__(self):
        super().__init__()

        # sprite setup
        self.visible_sprites = pygame.sprite.Group()

        self.player = Player(100, 100, [self.visible_sprites])

        # UI setup
        self.create_map()
        self.ui = gui.UIManager(self.display_surface.get_size())

        # fixme: debug only
        self.debug = []
        self.debug += debug_player(self.ui, self.player)

    def create_map(self):
        pass

    def process_events(self, event: pygame.event.Event):
        self.ui.process_events(event)

    def run(self):
        self.ui.update(pygame.time.get_ticks() / 1000)
        self.visible_sprites.update()

        for info in self.debug:
            info.update()

        self.visible_sprites.draw(self.display_surface)
        self.ui.draw_ui(self.display_surface)
