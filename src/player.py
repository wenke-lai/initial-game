from collections import defaultdict
from enum import Enum, auto
from typing import Literal

import pygame

from src.components.system import MouseAutoMoveSystem, MoveDirection


class PlayerAction(Enum):
    STAND = auto()
    WALK = auto()
    RUN = auto()
    JUMP = auto()
    PUSH = auto()
    PULL = auto()


# todo: refactor to a config file, this is dependent on the asset sources
FRAME_WIDTH = 64
FRAME_HEIGHT = 64
ANIMATION_MAPPINGS = {
    PlayerAction.STAND: {
        MoveDirection.DOWN: [(0, 0)],
        MoveDirection.UP: [(0, 1)],
        MoveDirection.RIGHT: [(0, 2)],
        MoveDirection.LEFT: [(0, 3)],
    },
    PlayerAction.PUSH: {
        MoveDirection.DOWN: [(1, 0), (2, 0)],
        MoveDirection.UP: [(1, 1), (2, 1)],
        MoveDirection.RIGHT: [(1, 2), (2, 2)],
        MoveDirection.LEFT: [(1, 3), (2, 3)],
    },
    PlayerAction.PULL: {
        MoveDirection.DOWN: [(3, 0), (4, 0)],
        MoveDirection.UP: [(3, 1), (4, 1)],
        MoveDirection.RIGHT: [(3, 2), (4, 2)],
        MoveDirection.LEFT: [(3, 3), (4, 3)],
    },
    PlayerAction.JUMP: {
        MoveDirection.DOWN: [(5, 0), (6, 0), (7, 0), (5, 0)],
        MoveDirection.UP: [(5, 1), (6, 1), (7, 1), (5, 1)],
        MoveDirection.RIGHT: [(5, 2), (6, 2), (7, 2), (5, 2)],
        MoveDirection.LEFT: [(5, 3), (6, 3), (7, 3), (5, 3)],
    },
    PlayerAction.WALK: {
        MoveDirection.DOWN: [(0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4)],
        MoveDirection.UP: [(0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5)],
        MoveDirection.RIGHT: [(0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6)],
        MoveDirection.LEFT: [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7)],
    },
    PlayerAction.RUN: {
        MoveDirection.DOWN: [(0, 4), (1, 4), (6, 4), (3, 4), (4, 4), (7, 4)],
        MoveDirection.UP: [(0, 5), (1, 5), (6, 5), (3, 5), (4, 5), (7, 5)],
        MoveDirection.RIGHT: [(0, 6), (1, 6), (6, 6), (3, 6), (4, 6), (7, 6)],
        MoveDirection.LEFT: [(0, 7), (1, 7), (6, 7), (3, 7), (4, 7), (7, 7)],
    },
}
UNDERWEARS = {
    "a": "1 outfit/char_a_p1_1out_boxr_v01.png",
    "b": "1 outfit/char_a_p1_1out_undi_v01.png",
}
HAIRS = {
    "a": "4 hair/char_a_p1_4har_dap1_v01.png",
    "b": "4 hair/char_a_p1_4har_bob1_v01.png",
}
OUTFITS = {
    "a": "1 outfit/char_a_p1_1out_fstr_v04.png",
    "b": "1 outfit/char_a_p1_1out_pfpn_v04.png",
}
HATS = {
    "a": "5 hat/char_a_p1_5hat_pfht_v04.png",
    "b": "5 hat/char_a_p1_5hat_pnty_v04.png",
}


def load_animations(body_type: Literal["a", "b"], mappings: dict, has_outfit):
    sheet_path = "src/assets/character/images/"

    surface_sheet = pygame.image.load(sheet_path + "character.png").convert_alpha()
    underwear_sheet = pygame.image.load(
        sheet_path + UNDERWEARS[body_type]
    ).convert_alpha()
    hair_sheet = pygame.image.load(sheet_path + HAIRS[body_type]).convert_alpha()

    if has_outfit:
        outfit_sheet = pygame.image.load(
            sheet_path + OUTFITS[body_type]
        ).convert_alpha()
        hat_sheet = pygame.image.load(sheet_path + HATS[body_type]).convert_alpha()

    animations = defaultdict(lambda: defaultdict(list))
    for action, directions in mappings.items():
        for direction, coordinates in directions.items():
            for x, y in coordinates:
                size = (x * FRAME_WIDTH, y * FRAME_HEIGHT, FRAME_WIDTH, FRAME_HEIGHT)

                character = surface_sheet.subsurface(*size)
                underwear = underwear_sheet.subsurface(*size)
                character.blit(underwear, (0, 0))
                hair = hair_sheet.subsurface(*size)
                character.blit(hair, (0, 0))

                if has_outfit:
                    outfit = outfit_sheet.subsurface(*size)
                    character.blit(outfit, (0, 0))
                    hat = hat_sheet.subsurface(*size)
                    character.blit(hat, (0, 0))

                # after merge, convert to display format
                character = character.convert_alpha()

                animations[direction][action].append(
                    # after scaling, convert to display format
                    pygame.transform.scale2x(character).convert_alpha()
                )

    return animations  # {PlayerDirection: {PlayerAction: [python.Surface]}


class Player(pygame.sprite.Sprite):
    def __init__(
        self,
        pos: list[int, int],
        body_type: str,
        groups: list[pygame.sprite.Group],
        obstacle_sprites: pygame.sprite.Group,
        has_outfit: bool = False,
    ):
        super().__init__(groups)
        self.obstacle_sprites = obstacle_sprites

        # todo: retrieve the status from the database
        self.status = {"speed": 3}

        # movement
        self.move_system = MouseAutoMoveSystem(self, obstacle_sprites)
        self.direction = self.move_system.direction
        self.speed = self.status["speed"]

        # action
        self.action = PlayerAction.STAND

        # animation setup
        self.animations = load_animations(body_type, ANIMATION_MAPPINGS, has_outfit)
        self.frame_index = 0
        self.frame_speed = 0.15  # todo: enhance this by ANIMATION TIMING GUIDE

        self.image = self.animations[self.direction][self.action][self.frame_index]
        # create a rect from the mask instead of the image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.mask.get_bounding_rects()[0]
        self.rect.center = pos
        self.hitbox = self.rect.inflate(-10, -10)

        # systems

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LSHIFT]:
            self.speed = self.status["speed"] * 2.5
        else:
            self.speed = self.status["speed"]

    def status_update(self):
        # the action
        if self.move_system.vector.magnitude() == 0:
            self.action = PlayerAction.STAND
        else:
            if self.speed > self.status["speed"]:
                self.action = PlayerAction.RUN
            else:
                self.action = PlayerAction.WALK

    def animate(self):
        animations = self.animations[self.direction][self.action]
        self.frame_index += self.frame_speed
        if self.frame_index >= len(animations):
            self.frame_index = 0

        self.image = animations[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self):
        self.input()
        self.move_system.update()
        self.status_update()
        self.animate()

        screen = pygame.display.get_surface()
        for point in self.move_system.path:
            pygame.draw.rect(screen, "yellow", (point[0], point[1], 32, 32), 2)
