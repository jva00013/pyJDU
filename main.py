import arcade
from src.views import TitleView, DressingView


class Game:
    game_window: arcade.Window

    def setup(self):
        self.game_window = arcade.Window(width=1336, height=768, title="Jagger Dress Up")

    def run(self):
        arcade.set_background_color((255, 181, 253))
        title_view = DressingView()
        self.game_window.show_view(title_view)
        title_view.setup()
        self.game_window.run()


if __name__ == "__main__":
    game = Game()
    game.setup()
    game.run()
