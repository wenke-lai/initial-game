from enum import Enum

import pygame

from src import settings
from src.components.algorithm import breadth_first_search


class MoveDirection(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class MoveSystem:
    def __init__(
        self,
        sprite: pygame.sprite.Sprite,
        collision_sprites: pygame.sprite.Group = None,
    ):
        self.sprite = sprite
        self.vector = pygame.math.Vector2()
        self.collision_sprites = collision_sprites
        self.direction = MoveDirection.DOWN

    def input(self):
        raise NotImplementedError("This method must be implemented in a subclass")

    def move(self):
        if self.vector.magnitude() == 0:
            return

        preview_pos = pygame.math.Vector2(self.sprite.hitbox.topleft)
        move_vector = pygame.math.Vector2(self.vector.normalize() * self.sprite.speed)
        self.sprite.hitbox.topleft += move_vector
        self.collisions(preview_pos)
        self.sprite.rect.center = self.sprite.hitbox.center

    def collisions(self, preview_pos: pygame.math.Vector2):
        for sprite in self.collision_sprites:
            if sprite.hitbox.colliderect(self.sprite.hitbox):
                if self.vector.x != 0:
                    self.sprite.hitbox.x = preview_pos.x
                if self.vector.y != 0:
                    self.sprite.hitbox.y = preview_pos.y

    def update_direction(self):
        if self.vector.x > 0:
            self.direction = MoveDirection.RIGHT
        elif self.vector.x < 0:
            self.direction = MoveDirection.LEFT
        elif self.vector.y > 0:
            self.direction = MoveDirection.DOWN
        elif self.vector.y < 0:
            self.direction = MoveDirection.UP
        else:
            # do-nothing (vector.x == vector.y == 0)
            pass

    def update(self):
        self.input()
        self.move()
        self.update_direction()


class ArrowMoveSystem(MoveSystem):
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.vector.y = -1
        elif keys[pygame.K_DOWN]:
            self.vector.y = 1
        else:
            self.vector.y = 0
        if keys[pygame.K_LEFT]:
            self.vector.x = -1
        elif keys[pygame.K_RIGHT]:
            self.vector.x = 1
        else:
            self.vector.x = 0


class WASDMoveSystem(MoveSystem):
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.vector.y = -1
        elif keys[pygame.K_s]:
            self.vector.y = 1
        else:
            self.vector.y = 0
        if keys[pygame.K_a]:
            self.vector.x = -1
        elif keys[pygame.K_d]:
            self.vector.x = 1
        else:
            self.vector.x = 0


class MouseMoveSystem(MoveSystem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.mouse_pos = None

    def input(self):
        if pygame.mouse.get_pressed()[0]:
            self.mouse_pos = pygame.mouse.get_pos()

    def update_distance_direction(self):
        if self.mouse_pos is None:
            return

        current_pos = pygame.math.Vector2(self.sprite.hitbox.center)
        if current_pos == self.mouse_pos:
            self.mouse_pos = None
            self.vector = pygame.math.Vector2()
        elif current_pos.distance_to(self.mouse_pos) < 2:
            self.sprite.hitbox.center = self.mouse_pos
            self.sprite.rect.center = self.sprite.hitbox.center
            self.mouse_pos = None
            self.vector = pygame.math.Vector2()
        else:
            self.vector = self.mouse_pos - current_pos

    def move(self):
        self.update_distance_direction()
        super().move()


class MouseAutoMoveSystem(MoveSystem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.collision_sprites is None:
            self.collision_sprites = pygame.sprite.Group()

        self.path = []

    def _find_path(self, target_pos):
        target_x, target_y = target_pos
        start = (
            int(self.sprite.hitbox.x // settings.GRID_SIZE),
            int(self.sprite.hitbox.y // settings.GRID_SIZE),
        )
        end = (
            target_x // settings.GRID_SIZE,
            target_y // settings.GRID_SIZE,
        )
        return breadth_first_search(
            start,
            end,
            self.collision_sprites,
            settings.GRID_SIZE,
            settings.WINDOW_WIDTH,
            settings.WINDOW_HEIGHT,
        )

    def input(self):
        if pygame.mouse.get_pressed()[0]:
            self.path = self._find_path(pygame.mouse.get_pos())

    def move(self):
        if not self.path:
            return

        source_pos = pygame.math.Vector2(self.sprite.hitbox.topleft)
        target_pos = pygame.math.Vector2(self.path[0])
        if source_pos.distance_to(target_pos) > self.sprite.speed:
            self.vector = (target_pos - source_pos).normalize()
            self.sprite.hitbox.topleft = source_pos + self.vector * self.sprite.speed
            if self.collisions():
                self.sprite.hitbox.topleft = source_pos
        else:
            self.vector = target_pos
            self.sprite.hitbox.topleft = target_pos
            self.path.pop(0)
        self.sprite.rect.center = self.sprite.hitbox.center

    def collisions(self):
        for sprite in self.collision_sprites:
            if self.sprite.hitbox.colliderect(sprite.hitbox):
                return True
        return False

    def update(self):
        super().update()

        screen = pygame.display.get_surface()
        for point in self.move_system.path:
            pygame.draw.rect(screen, "yellow", (point[0], point[1], 32, 32), 2)
