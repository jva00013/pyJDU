import arcade
from src.views import DoneView

if __name__ == "__main__":
    gameWindow = arcade.Window(width=800, height=600, title="Jagger Dress Up")
    gameWindow.show_view(DoneView())
    gameWindow.run()