import pygame
from scenes.scene import Scene
from scenes.game_board import GameBoard
from ui.button import Button
from ui.text_box import TextBox
from ui.text_label import TextLabel
from entities.dice import Dice
import numpy as np
import time
import os
import random
import glob

class CharacterCreation(Scene):
    def __init__(self, game_manager):
        super().__init__(game_manager, bg_color=(204,230,207)) # always need to do this

        # minimum number of players needed to start the game
        self.min_players = 2

        # Screen dimensions
        self.screen_width = game_manager.screen.get_width()
        self.screen_height = game_manager.screen.get_height()

        self.character_list = []

        # UI Elements
        self.title_label = TextLabel(self.screen_width * 0.5, self.screen_height * 0.25,
                                    "Character Creator")
        self.new_character_button = Button(self.screen_width * 0.33, self.screen_height * 0.7,
                                    "New Character", self.new_character, button_color="LIGHTRED")
        self.new_ai_button = Button(self.screen_width * 0.66, self.screen_height * 0.7,
                                    "New AI Character", self.new_ai_character, button_color="WHITE", text_color="BLACK")
        self.play_button = Button(self.screen_width * 0.5, self.screen_height * 0.85,
                                  "Play!", self.play_game, button_color="DARKGREEN", width=468)

        self.display_entities = []

        # Add entities to scene so they are handled automatically
        self.add_entity(self.title_label)
        self.add_entity(self.new_character_button)
        self.add_entity(self.new_ai_button)
        self.display_entities.append(self.new_character_button)
        self.display_entities.append(self.new_ai_button)

        # Get tokens
        self.token_list = [os.path.basename(f) for f in glob.glob("assets/tokens/*.png")]
        random.shuffle(self.token_list)
    
    def display_options(self):
        self.add_entity(self.new_character_button)
        self.add_entity(self.new_ai_button)
        self.display_entities.append(self.new_character_button)
        self.display_entities.append(self.new_ai_button)

        # Play option
        if len(self.character_list) >= self.min_players:
            self.add_entity(self.play_button)
            self.display_entities.append(self.play_button)
    
    def play_game(self):
        self.game_manager.change_scene(GameBoard(self.game_manager, self.character_list))

    def display_character_list(self):
        self.clear_display()
        self.display_options()

        def gen_spacing_scalars(n):
            if n <= 0:
                return []
            return [(i + 1) / (n + 1) for i in range(n)]

        num_chars = len(self.character_list)
        x_scalars = gen_spacing_scalars(num_chars)
        for i in range(len(x_scalars)):
            display_entity = TextLabel(self.screen_width * x_scalars[i],
                                       self.screen_height * 0.5, self.character_list[i]["name"])
            self.add_entity(display_entity)
            self.display_entities.append(display_entity)

    def add_to_char_list(self, name):
        # decide token
        token = "assets/tokens/" + self.token_list[len(self.character_list) % len(self.token_list)]

        self.character_list.append({
            "name": name,
            "token": token
        })
        self.display_character_list()
    
    def new_character(self):
        self.clear_display()

        # Get player name
        player_name_input = TextBox(self.screen_width * 0.5, self.screen_height * 0.5,
                                    placeholder="Your name...", on_submit=self.add_to_char_list)
        self.add_entity(player_name_input)
        self.display_entities.append(player_name_input)

    def new_ai_character(self):
        ai_prefixes = ["Sir", "Mr", "Dr", "Cap", "Prof", "Agent", "Lord", "Lady", "Col",
                       "Maj", "Baron", "Dame", "Count","Countess", "Duke", "Duchess", "Marshal",
                       "Admiral", "Commander", "Chief", "Mrs"]
        token_name = self.token_list[len(self.character_list) % len(self.token_list)].replace(".png", "").capitalize()
        self.add_to_char_list(f"{random.choice(ai_prefixes)} {token_name}")

    def clear_display(self):
        for e in self.display_entities:
            self.remove_entity(e)
        self.display_entities = []