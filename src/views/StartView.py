import arcade

class StartView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_draw(self):
        self.clear()
