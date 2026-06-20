from scenes.events.scene_event import SceneEvent
from entities.card import Card
import json
import random

class ChanceEvent(SceneEvent):
    def __init__(self, scene, player, space):
        super().__init__(scene, player, space)
        if self.space.text == "Pot Luck":
            filename = "pot_luck_data.json"
            title = "Pot Luck"
            color = "LIGHTBLUE"
        else:
            filename = "opp_knocks_data.json"
            title = "Opportunity Knocks"
            color = "ORANGE"
        with open(filename, 'r') as file:
            chance_data = json.load(file)
        card_data = random.choice(chance_data)
        self.card = Card(scene, title, card_data["description"], self.confirm, color)
        self.action = card_data["action"]
        self.value = card_data["value"]
        self.destination = card_data["movement_location"]

    def confirm(self):
        if self.card.side == 0:
            self.card.side = 1
        else:
            eval(f"self.{self.action}()")
            self.scene.remove_entity(self.card)

    def on_land(self):
        """SCENE EVENT: Called when a player lands on this space"""
        # handle chance case
        self.scene.add_entity(self.card)
        self.scene.hide_player_turn_ui()

    def on_pass(self):
        """SCENE EVENT: Called when a player passes this space"""
        pass

    # CHANCE ACTIONS referred to by the json files
    def receive_money(self):
        self.player.bank_balance += self.value
        self.scene.next_turn()

    def receive_from_all(self):
        for p in self.scene.players:
            if p["game_agent"] != self.player:
                p["game_agent"].bank_balance -= self.value
                self.player.bank_balance += self.value
        self.scene.next_turn()

    def go_to_jail(self):
        self.player.go_to_jail()
        self.scene.next_turn()

    def set_space(self):
        head_space = self.scene.spaces.get_head_space()
        curr_space = head_space.next_space
        while curr_space != head_space:
            if curr_space.text.lower() == self.destination.lower():
                target_space = curr_space
                break
            curr_space = curr_space.next_space
        self.player.set_current_space(target_space)
        self.scene.next_turn()

    def jump_to(self):
        num_jumps = 0
        curr_space = self.space
        while True:
            if curr_space.text.lower() == self.destination.lower():
                break
            curr_space = curr_space.next_space
            num_jumps += 1
        self.player.jump_spaces(num_jumps)

    def jump(self):
        self.player.jump_spaces(self.value)

    def housing_money(self):
        num_houses = 0
        num_hotels = 0
        head_space = self.scene.spaces.get_head_space()
        curr_space = head_space.next_space
        while curr_space != head_space:
            if curr_space.space_type == "PROPERTY" and curr_space.property.owner == self.player:
                if curr_space.property.rent_idx <= 4:
                    num_houses += curr_space.property.rent_idx
                elif curr_space.property.rent_idx == 5:
                    num_hotels += 1
            curr_space = curr_space.next_space
        self.player.bank_balance += num_houses * self.value[0] + num_hotels * self.value[1]
        self.scene.next_turn()

    def parking_money(self):
        self.scene.jackpot += self.value
        self.player.bank_balance -= self.value
        self.scene.next_turn()