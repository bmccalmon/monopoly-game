from scenes.events.scene_event import SceneEvent

class JackpotEvent(SceneEvent):
    def __init__(self, scene, player, space):
        super().__init__(scene, player, space)

    def on_land(self):
        """SCENE EVENT: Called when a player lands on this space"""
        self.player.bank_balance += self.scene.jackpot
        self.scene.jackpot = 0
        self.scene.next_turn()

    def on_pass(self):
        """SCENE EVENT: Called when a player passes this space"""
        pass