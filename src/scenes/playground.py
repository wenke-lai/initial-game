import random
from itertools import product

import pygame
import pygame_gui as gui

from src import settings
from src.components.scene import BaseScene
from src.player import Player, debug_player


def random_pos(
    width: int = settings.WINDOW_WIDTH,
    height: int = settings.WINDOW_HEIGHT,
    margin: int = 64 * 2,
):
    return (
        random.randint(margin, width - margin),
        random.randint(margin, height - margin),
    )


def create_grid(screen: pygame.Surface):
    for x in range(0, settings.WINDOW_WIDTH, settings.GRID_SIZE):
        pygame.draw.line(screen, "white", (x, 0), (x, settings.WINDOW_HEIGHT))
    for y in range(0, settings.WINDOW_HEIGHT, settings.GRID_SIZE):
        pygame.draw.line(screen, "white", (0, y), (settings.WINDOW_WIDTH, y))


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)

        self.image = pygame.Surface((50, 50))
        self.image.fill("red")
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-10, -10)


class Scene(BaseScene):
    def __init__(self):
        super().__init__()

        # sprite setup
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

        self.player = Player(
            (100, 100),
            "a",
            [self.visible_sprites],
            self.obstacle_sprites,
        )

        # UI setup
        self.create_map()
        self.ui = gui.UIManager(self.display_surface.get_size())

        # fixme: debug only
        self.debug = []
        self.debug += debug_player(self.ui, self.player)

    def create_map(self):
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
        create_grid(self.display_surface)

        self.ui.update(pygame.time.get_ticks() / 1000)
        self.visible_sprites.update()

        for info in self.debug:
            info.update()

        self.visible_sprites.draw(self.display_surface)
        self.ui.draw_ui(self.display_surface)


if __name__ == "__main__":
    create_grid()
