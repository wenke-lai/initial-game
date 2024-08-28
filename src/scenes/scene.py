import pygame


class BaseScene:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False

        # sprite groups
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

        self.sound = None

    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def play_sound(self):
        if self.sound:
            self.sound.play()

    def run(self):
        self.play_sound()
