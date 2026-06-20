import pygame
from scenes.scene import Scene
from scenes.character_creation import CharacterCreation
from ui.button import Button
from ui.text_label import TextLabel

class MainMenu(Scene):
    def __init__(self, game_manager):
        super().__init__(game_manager, bg_color=(204,230,207)) # always need to do this

        # Screen dimensions
        screen_width = game_manager.screen.get_width()
        screen_height = game_manager.screen.get_height()

        # UI Elements
        self.title_label = TextLabel(screen_width * 0.5, screen_height * 0.25,
                                     "Main Menu")
        self.start_button = Button(screen_width * 0.25, screen_height * 0.5,
                                   "New Game", self.start_game)
        self.quit_button = Button(screen_width * 0.75, screen_height * 0.5,
                                  "Quit", self.quit_game)

        # Add entities to scene so they are handled automatically
        self.add_entity(self.title_label)
        self.add_entity(self.start_button)
        self.add_entity(self.quit_button)

    def start_game(self):
        """BUTTON ACTION: Switch to the CharacterCreation scene when clicking start."""
        self.game_manager.change_scene(CharacterCreation(self.game_manager))

    def quit_game(self):
        """BUTTON ACTION: Quit the game."""
        self.game_manager.running = False
