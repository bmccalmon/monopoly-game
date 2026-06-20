
class SceneEvent():
    def __init__(self, scene, player, space):
        self.scene = scene
        self.player = player
        self.space = space

    def on_land(self):
        pass

    def on_pass(self):
        pass