import arcade
from src.views import TitleView
from time import time

class Game:
    game_window: arcade.Window

    def setup(self):
        self.game_window = arcade.Window(width=1366, height=768, title="Jagger Dress Up")

    def run(self):
        arcade.set_background_color((255, 181, 253))
        title_view = TitleView()
        t0 = time()
        title_view.setup()
        t1 = time()
        print(f"Setup first view: {t1-t0}")
        self.game_window.show_view(title_view)
        self.game_window.run()


if __name__ == "__main__":
    game = Game()
    game.setup()
    game.run()

