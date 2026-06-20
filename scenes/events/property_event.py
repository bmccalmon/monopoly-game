from scenes.events.scene_event import SceneEvent
from ui.text_label import TextLabel
from ui.button import Button
from ui.text_box import TextBox
import time

"""
BUYING PROPERTIES:
Whenever you land on an unowned property you may buy that property from the Bank at its printed price.
If you do not wish to buy the property, the Bank sells it through auction to the highest bidder.
The high bidder pays the Bank the amount of the bid in cash and receives the property.

Any player, including the one who declined the option to buy it at the printed price, may bid.
Bidding may start at any price.
"""

class PropertyEvent(SceneEvent):
    def __init__(self, scene, player, space):
        super().__init__(scene, player, space)

        self.property = self.space.property

        self.property_name = TextLabel(scene.screen_width * 0.5, scene.screen_height * 0.3, space.text)
        self.property_value = TextLabel(scene.screen_width * 0.5, scene.screen_height * 0.35,
                                        f"£{self.property.get_value()}")
        self.property_owner = TextLabel(scene.screen_width * 0.5, scene.screen_height * 0.34, "")
        self.query = TextLabel(scene.screen_width * 0.5, scene.screen_width * 0.4,
                               f"{player.name}, what do you want to do?")
        self.buy_button = Button(scene.screen_width * 0.38, scene.screen_height * 0.5,
                                 "BUY", self.buy_property, width=100, button_color="GREEN")
        self.auction_button = Button(scene.screen_width * 0.6, scene.screen_height * 0.5,
                                 "SEND TO AUCTION", self.auction_property, width=230)
        self.tax_query = TextLabel(scene.screen_width * 0.5, scene.screen_height * 0.4, "")
        self.tax_button = Button(scene.screen_width * 0.5, scene.screen_height * 0.5,
                                 "PAY RENT", self.pay_tax)
        self.continue_button = Button(scene.screen_width * 0.5, scene.screen_height * 0.5,
                                 "CONTINUE", self.do_nothing)
        
        # Auctioning

        # Prepare the auction queue, starting at the landing player
        self.player_auction_list = []
        curr_i = self.scene.player_turn
        for _ in range(len(self.scene.players)):
            self.player_auction_list.append([self.scene.players[curr_i]["game_agent"],
                                              0, False]) # [game_agent, total bid, skipped?]
            curr_i = (curr_i + 1) % len(self.scene.players)
        self.auction_turn = 0
        self.highest_bidder_idx = None

        self.auction_query = TextLabel(scene.screen_width * 0.5, scene.screen_height * 0.4, "")
        self.skip_turn_button = Button(self.scene.screen_width * 0.6, self.scene.screen_height * 0.5,
                                "SKIP TURN", self.auction_skip_turn, width=230)
        self.bid_button = Button(self.scene.screen_width * 0.33, self.scene.screen_height * 0.5,
                                "NEW BID", self.auction_bid, width=155, button_color="GREEN")
        self.bid_field = TextBox(self.scene.screen_width * 0.33, self.scene.screen_height * 0.57, width=50)
        self.total_bid_label = TextLabel(self.scene.screen_width * 0.5, self.scene.screen_height * 0.64, "")
        self.highest_bid_label = TextLabel(self.scene.screen_width * 0.6, self.scene.screen_height * 0.57, "")

    def on_land(self):
        """SCENE EVENT: Called when a player lands on this space"""
        self.scene.add_entity(self.property_name)

        if not self.property.owner:
            self.scene.add_entity(self.query)
            self.scene.add_entity(self.buy_button)
            self.scene.add_entity(self.auction_button)
            self.scene.add_entity(self.property_value)
        else:
            self.property_owner.text = f"Owned by {self.property.owner.name}."
            if self.property.owner == self.player:
                self.scene.add_entity(self.continue_button)
                self.tax_query.text = f"You own this property."
            else:
                self.scene.add_entity(self.tax_button)
                self.tax_query.text = f"{self.property.owner.name} owns this property. You owe £{self.property.get_base_tax() * self.property.get_tax_multiplier()}."
            self.scene.add_entity(self.tax_query)

    def on_pass(self):
        """SCENE EVENT: Called when a player passes this space"""
        pass

    def do_nothing(self):
        self.clear_ui()
        self.scene.next_turn()

    def pay_tax(self):
        rent = self.property.get_base_tax() * self.property.get_tax_multiplier()
        self.player.bank_balance -= rent
        self.property.owner.bank_balance += rent

        self.clear_ui()
        self.scene.next_turn()

    # AUCTION FUNCTIONS
    def auction_update_ui(self):
        self.auction_query.text = f"{self.player_auction_list[self.auction_turn][0].name}'s turn to bid."
        self.total_bid_label.text = f"{self.player_auction_list[self.auction_turn][0].name}'s bid: £{self.player_auction_list[self.auction_turn][1]}"
        if self.highest_bidder_idx is None:
            self.highest_bid_label.text = f"Highest bid: £0"
        else:
            self.highest_bid_label.text = f"Highest bid: £{self.player_auction_list[self.highest_bidder_idx][1]} ({self.player_auction_list[self.highest_bidder_idx][0].name})"

    def auction_next_turn(self):
        end_auction = True
        for s in self.player_auction_list:
            if not s[2]:
                end_auction = False
                break
        if end_auction:
            self.auction_exit()
            return
        self.auction_turn = (self.auction_turn + 1) % len(self.scene.players)
        self.bid_field.text = ""
        self.auction_update_ui()

    def auction_skip_turn(self):
        self.player_auction_list[self.auction_turn][2] = True
        self.auction_next_turn()

    def auction_bid(self):
        if self.bid_field.text:
            # First bid?
            if self.highest_bidder_idx is None:
                self.highest_bidder_idx = self.auction_turn
            # Bid high enough?
            if int(self.bid_field.text) <= self.player_auction_list[self.highest_bidder_idx][1]:
                return
            # Player have enough money?
            if self.player_auction_list[self.auction_turn][0].bank_balance < int(self.bid_field.text):
                return
            self.highest_bidder_idx = self.auction_turn
            self.player_auction_list[self.auction_turn][1] = int(self.bid_field.text)
            self.player_auction_list[self.auction_turn][2] = False
            self.auction_next_turn()

    def auction_exit(self):
        # Highest bidder gets property
        if not self.highest_bidder_idx is None:
            self.player_auction_list[self.highest_bidder_idx][0].bank_balance -= self.player_auction_list[self.highest_bidder_idx][1]
            self.property.owner = self.player_auction_list[self.highest_bidder_idx][0]

        self.clear_ui()
        self.scene.next_turn()
    
    def auction_property(self):
        # Remove the UI
        self.clear_ui()

        self.auction_update_ui()
        self.scene.add_entity(self.auction_query)
        self.scene.add_entity(self.property_name)
        self.scene.add_entity(self.property_value)
        self.scene.add_entity(self.skip_turn_button)
        self.scene.add_entity(self.bid_button)
        self.scene.add_entity(self.bid_field)
        self.scene.add_entity(self.total_bid_label)
        self.scene.add_entity(self.highest_bid_label)

    def buy_property(self):
        # Set ownership if have enough money
        property_price = self.property.get_value()
        player_balance = self.player.bank_balance
        if player_balance >= property_price:
            self.player.bank_balance -= property_price
            self.property.owner = self.player

        # Remove the UI
        self.clear_ui()

        # Trigger next turn
        self.scene.next_turn() # ALWAYS NEED TO DO THIS ONCE DONE

    def clear_ui(self):
        self.scene.remove_entity(self.property_name)
        self.scene.remove_entity(self.property_value)
        self.scene.remove_entity(self.query)
        self.scene.remove_entity(self.buy_button)
        self.scene.remove_entity(self.tax_query)
        self.scene.remove_entity(self.tax_button)
        self.scene.remove_entity(self.auction_button)
        self.scene.remove_entity(self.continue_button)
        self.scene.remove_entity(self.property_owner)
        self.scene.remove_entity(self.auction_query)
        self.scene.remove_entity(self.bid_button)
        self.scene.remove_entity(self.bid_field)
        self.scene.remove_entity(self.skip_turn_button)
        self.scene.remove_entity(self.total_bid_label)
        self.scene.remove_entity(self.highest_bid_label)