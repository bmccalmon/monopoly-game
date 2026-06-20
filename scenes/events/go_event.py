from scenes.events.scene_event import SceneEvent

class GoEvent(SceneEvent):
    def __init__(self, scene, player, space):
        super().__init__(scene, player, space)

    def on_land(self):
        """SCENE EVENT: Called when a player lands on this space"""
        # handle go case
        print(f"{self.player.name} landed on a GO space.")
        self.scene.next_turn()

    def on_pass(self):
        """SCENE EVENT: Called when a player passes this space"""
        self.player.bank_balance += self.space.pass_reward