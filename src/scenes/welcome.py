from .scene import BaseScene
from .ui import DebugOverlay


class Welcome(BaseScene):
    def __init__(self):
        super().__init__()

        self.ui = DebugOverlay()

    def run(self):
        super().run()

        self.ui.update()

        self.ui.append("Welcome to the game")
        self.ui.append("Welcome to the game", "red")
        self.ui.append("Welcome to the game", "green")

        self.ui.draw()

        # self.visible_sprites.draw()
        # self.visible_sprites.dupdate()
        ...
