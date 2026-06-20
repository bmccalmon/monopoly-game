from entities.entity import Entity
import pygame
import json

class Card(Entity):
    def __init__(self, scene, title, description, action, color="ORANGE"):
        super().__init__(scene.screen_width * 0.5, scene.screen_width * 0.5, 600, 300)
        self.scene = scene
        self.title = title
        self.description = description
        self.action = action
        with open("ui/colors.json", 'r') as file:
            colors = json.load(file)
        self.color = colors[color]
        self.side = 0

    def render(self, screen):
        if self.side == 0:
            # Card
            pygame.draw.rect(
                screen,
                self.color,
                self.rect
            )
            pygame.draw.rect(
                screen,
                (0,0,0),
                self.rect,
                2
            )
            # Title
            font = pygame.font.Font(None, 50 * int(self.camera_scale))
            text_surface = font.render(self.title, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)
        else:
            pygame.draw.rect(
                screen,
                (255, 255, 255),
                self.rect
            )
            # Top section
            top_rect = (self.rect.topleft[0], self.rect.topleft[1], self.rect.width, self.rect.height // 3)
            pygame.draw.rect(
                screen,
                self.color,
                top_rect
            )
            pygame.draw.rect(
                screen,
                (0, 0, 0),
                top_rect,
                2
            )
            # Rest
            pygame.draw.rect(
                screen,
                (0, 0, 0),
                self.rect,
                2
            )
            # Title
            font = pygame.font.Font(None, 50 * int(self.camera_scale))
            text_surface = font.render(self.title, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, (text_rect.topleft[0],
                        text_rect.topleft[1] - (self.rect.height // 3),
                        text_rect.width, text_rect.height))
            # Description
            font = pygame.font.Font(None, 30 * int(self.camera_scale))
            text_surface = font.render(self.description, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        mouse_over = self.rect.collidepoint(mouse_pos)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and mouse_over:
                self.action()