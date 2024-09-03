import pygame


class AttackSystem:
    def __init__(self, cooldown: int = 0):
        self.attacking = False
        self.attack_time = 0
        self.attack_cooldown = cooldown

    def attack(self):
        if not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()

    def cooldowns(self):
        if not self.attacking:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.attack_time > self.attack_cooldown:
            self.attacking = False

    def update(self):
        self.attack_cooldown += 1
