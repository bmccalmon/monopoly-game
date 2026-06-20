from scenes.events.scene_event import SceneEvent

class TaxesEvent(SceneEvent):
    def __init__(self, scene, player, space):
        super().__init__(scene, player, space)

    def on_land(self):
        """SCENE EVENT: Called when a player lands on this space"""
        print(f"{self.player.name} landed on a TAXES space.")
        self.player.bank_balance += self.space.pass_reward
        self.scene.next_turn()

    def on_pass(self):
        """SCENE EVENT: Called when a player passes this space"""
        pass