import pygame
from scenes.main_menu import MainMenu
import sys

class GameManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800))
        self.clock = pygame.time.Clock()
        self.running = True
        self.scene = MainMenu(self)  # Start with MainMenu
        self.debug_mode = True if len(sys.argv) >= 2 and sys.argv[1] == 'd' else False # enable/disable debug mode

        # Start music
        pygame.mixer.music.load('assets/audio/music/jazz1.mp3')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

    def change_scene(self, new_scene):
        """Switches to a new scene"""
        self.scene = new_scene

    def run(self):
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.scene.handle_events(events)
            self.scene.update()
            self.scene.render(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    GameManager().run()
