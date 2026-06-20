from entities.entity import Entity
import pygame 
import json

class UIElement(Entity):
    def __init__(self, x, y, width, height, text="", font_size=32, centered=True, text_color="BLACK"):
        super().__init__(x, y, width, height, centered=centered)
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        with open("ui/colors.json", 'r') as file:
            colors = json.load(file)
        self.text_color = colors[text_color]

    def render_text(self, screen):
        """Helper function to render text in the center of the element."""
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
