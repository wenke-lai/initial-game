import pygame
import pygame_gui as gui

from .scene import BaseScene
from .ui import DebugOverlay


class Welcome(BaseScene):
    def __init__(self):
        super().__init__()

        self.ui = DebugOverlay()

        # setup gui
        self.gui_manager = gui.UIManager((self.width, self.height))
        self.btn_start = gui.elements.UIButton(
            relative_rect=pygame.Rect(self.width // 2, self.height // 2, 100, 50),
            text="Start",
            manager=self.gui_manager,
        )

        # event status
        self.finished = False

    def process_events(self, event: pygame.event.Event):
        self.gui_manager.process_events(event)
        if self.btn_start.check_pressed():
            self.finished = True

    def run(self) -> str | None:
        super().run()

        self.gui_manager.update(pygame.time.get_ticks())
        self.ui.update()
        self.ui.append("Welcome to the game")
        self.ui.append("Welcome to the game", "red")
        self.ui.append("Welcome to the game", "green")

        self.ui.draw()
        self.gui_manager.draw_ui(self.display_surface)

        if self.finished:
            return "playground"
