import random

import pygame
import pygame_gui as gui

from src.components.scene import BaseScene
from src.player import Player, debug_player
from src import settings

def random_pos(width: int = settings.WINDOW_WIDTH, height: int = settings.WINDOW_HEIGHT, merge: int = 64 * 2):
    return (random.randint(0, width - merge), random.randint(0, height - merge))


def create_grid(groups, size: int = 10):
    mod_num = size * 2
    for x in range(0, settings.WINDOW_WIDTH, size):
        for y in range(0, settings.WINDOW_HEIGHT, size):
            if (x % mod_num == 0 and y % mod_num == 0) or (x % mod_num != 0 and y % mod_num != 0):
                AnchorPoint((x, y), groups)


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)

        self.image = pygame.Surface((50, 50))
        self.image.fill("red")
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)

class AnchorPoint(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)

        self.image = pygame.Surface((10,10), pygame.SRCALPHA)
        self.image.fill((125, 0, 0, 125))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 0)

class Scene(BaseScene):
    def __init__(self):
        super().__init__()

        # sprite setup
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

        self.player = Player((100, 100), "a", [self.visible_sprites], self.obstacle_sprites)

        # UI setup
        self.create_map()
        self.ui = gui.UIManager(self.display_surface.get_size())

        # fixme: debug only
        self.debug = []
        self.debug += debug_player(self.ui, self.player)

    def create_map(self):
        create_grid([self.visible_sprites])

        for _ in range(2):
            npc = Player(
                random_pos(),
                random.choice(["a", "b"]),
                [self.visible_sprites, self.obstacle_sprites],
                None,
                random.choice([True, False]),
            )
            if random.choice([True, False]):
                npc.input = lambda: None  # can do nothing
            npc.move = lambda: None  # can do actions but no movement

            Obstacle(random_pos(), [self.visible_sprites, self.obstacle_sprites])

    def process_events(self, event: pygame.event.Event):
        self.ui.process_events(event)

    def run(self):
        self.ui.update(pygame.time.get_ticks() / 1000)
        self.visible_sprites.update()

        for info in self.debug:
            info.update()

        self.visible_sprites.draw(self.display_surface)
        self.ui.draw_ui(self.display_surface)
