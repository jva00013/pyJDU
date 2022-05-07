import arcade
from src.views import DoneView

if __name__ == "__main__":
    gameWindow = arcade.Window(width=1366, height=768, title="Jagger Dress Up")
    done_view = DoneView()
    done_view.setup()
    gameWindow.show_view(done_view)
    gameWindow.run()
