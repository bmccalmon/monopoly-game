import pygame
from ui.ui_element import UIElement
import json
import colorsys

class Button(UIElement):
    def __init__(self, x, y, text, action, width=200, height=50, centered=True, text_color="WHITE", button_color="LIGHTRED"):
        super().__init__(x, y, width, height, text, centered=centered, text_color=text_color)
        self.action = action
        with open("ui/colors.json", 'r') as file:
            colors = json.load(file)
        self.button_color = colors[button_color]

        # handle hover colors
        r, g, b = self.button_color
        r_norm, g_norm, b_norm = r / 255.0, g / 255.0, b / 255.0
        h, s, v = colorsys.rgb_to_hsv(r_norm, g_norm, b_norm)
        v = min(1.0, v + 0.2)
        hover_r, hover_g, hover_b = colorsys.hsv_to_rgb(h, s, v)
        self.hover_color = (
            int(hover_r * 255),
            int(hover_g * 255),
            int(hover_b * 255)
        )
        
        self.current_color = self.button_color

    def handle_events(self, events):
        """Detects clicks and triggers action."""
        mouse_pos = pygame.mouse.get_pos()
        mouse_over = self.rect.collidepoint(mouse_pos)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and mouse_over:
                self.action()  # Execute assigned function

        # Change color on hover
        self.current_color = self.hover_color if mouse_over else self.button_color

    def render(self, screen):
        pygame.draw.rect(screen, self.current_color, self.rect)
        self.render_text(screen)
