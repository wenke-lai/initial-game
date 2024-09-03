import webbrowser

import pygame
import pygame_gui as gui

from src.components.scene import BaseScene


class Welcome(BaseScene):
    def __init__(self):
        super().__init__()

        # event status
        self.finished = False

        # setup gui
        self.gui_manager = gui.UIManager(
            (self.width, self.height),
            theme_path="src/scenes/welcome_theme.json",
        )
        self.create_ui()

    def create_ui(self):
        gui.elements.UIButton(
            relative_rect=pygame.Rect(0, 0, 100, 50),
            text="Start",
            manager=self.gui_manager,
            anchors={"center": "center"},
            command=self._start_the_game,
        )
        gui.elements.UILabel(
            relative_rect=pygame.Rect(0, -60, 400, 60),
            text="Welcome to the game",
            manager=self.gui_manager,
            anchors={"center": "center"},
        )
        gui.elements.UIButton(
            relative_rect=pygame.Rect(0, 120, 100, 50),
            text="Login",
            manager=self.gui_manager,
            anchors={"center": "center"},
            command=self._login,
        )

    def _start_the_game(self):
        self.finished = True

    def _login(self):
        try:
            default_browser = webbrowser.get("windows-default")
            default_browser.open("https://www.google.com")
        except webbrowser.Error as exc:
            print("launch browser failed")
            print(exc)

    def process_events(self, event: pygame.event.Event):
        self.gui_manager.process_events(event)

        # fixme: debug only
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.finished = True

    def run(self) -> str | None:
        super().run()

        self.gui_manager.update(pygame.time.get_ticks())
        self.gui_manager.draw_ui(self.display_surface)

        if self.finished:
            return "playground"
