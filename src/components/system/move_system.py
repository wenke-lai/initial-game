import pygame


class MoveSystem:
    def __init__(
        self,
        sprite: pygame.sprite.Sprite,
        collision_sprites: pygame.sprite.Group = None,
    ):
        self.sprite = sprite
        self.vector = pygame.math.Vector2()
        self.collision_sprites = collision_sprites

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

    def update(self):
        self.input()
        self.move()


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
