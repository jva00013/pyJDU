import arcade
from src.views import TitleView


class Game:
    game_window: arcade.Window

    def setup(self):
        self.game_window = arcade.Window(width=1366, height=768, title="Jagger Dress Up")

    def run(self):
        title_view = TitleView()
        title_view.setup()
        self.game_window.show_view(title_view)
        self.game_window.run()


if __name__ == "__main__":
    game = Game()
    game.setup()
    game.run()

