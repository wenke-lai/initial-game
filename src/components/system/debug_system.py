import pygame


class AnchorPointSystem(pygame.sprite.Sprite):
    def __init__(
        self,
        sprite: pygame.sprite.Sprite,
        groups,
        color: str = "red",
        size: int = 10,
    ):
        super().__init__(groups)
        self.sprite = sprite

        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=self.sprite.rect.center)

        self.hitbox = self.rect.inflate(0, 0)

    def update(self):
        self.rect.center = self.sprite.rect.center
        self.hitbox.center = self.rect.center
