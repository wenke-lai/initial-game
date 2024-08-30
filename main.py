import sys
from importlib import import_module

import pygame

from src import colors, settings
from src.scenes import Welcome


class Game:
    def __init__(self):
        # general setup
        pygame.init()
        pygame.mixer.init()

        # game setup
        self.screen = pygame.display.set_mode(
            (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
        )
        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()

        # scene setup
        self.scene = Welcome()

    def change_scene(self, scene_name: str):
        scene_module = import_module(f"src.scenes.{scene_name}")
        self.scene = scene_module.Scene()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.scene.toggle_menu()

                    # ! delete me: just for debugging
                    if event.key == pygame.K_F4:
                        pygame.quit()
                        sys.exit()

                self.scene.process_events(event)

            self.screen.fill(colors.BACKGROUND)
            # scene logic
            scene_name = self.scene.run()
            if scene_name:
                self.change_scene(scene_name)

            pygame.display.flip()
            self.clock.tick(settings.FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
