import pygame
import json
from entities.entity import Entity
from properties import Property

class Space(Entity):
    def __init__(self, scene, x, y, size, space_type, pass_reward, text, icon, color):
        super().__init__(x, y, size, size, centered=False)
        self.space_type = space_type
        self.pass_reward = pass_reward
        self.text = text
        self.icon = icon
        self.color = color
        self.property = None
        self.next_space = None
        self.quadrant_idx = 1
        self.scene = scene

        self.show_house_prompt = False
        self.show_jackpot = False

        self.house_price = None
        # Prices hard coded for now
        if self.color == "BROWN" or self.color == "BLUE":
            self.house_price = 50
        elif self.color == "PURPLE" or self.color == "ORANGE":
            self.house_price = 100
        elif self.color == "RED" or self.color == "YELLOW":
            self.house_price = 150
        elif self.color == "GREEN" or self.color == "DARKBLUE":
            self.house_price = 200

        return None

    def player_owns_group(self):
        """Returns true if the player owns all the properties within the color group, false otherwise"""
        if self.scene.players[self.scene.player_turn]["game_agent"] != self.property.owner:
            return False
        curr_space = self.next_space
        while curr_space != self:
            if curr_space.color == self.color:
                if self.scene.players[self.scene.player_turn]["game_agent"] != curr_space.property.owner:
                    return False
            curr_space = curr_space.next_space
        return True
    
    def would_be_even(self):
        """Returns false if houses aren't being built evenly"""
        curr_space = self.next_space
        while curr_space != self:
            if curr_space.color == self.color and curr_space.space_type == "PROPERTY":
                if abs(curr_space.property.rent_idx - (self.property.rent_idx + 1)) > 1:
                    return False
            curr_space = curr_space.next_space
        return True
    
    def handle_events(self, events):
        """When a space is clicked"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_over = self.rect.collidepoint(mouse_pos)
        if self.space_type == "PROPERTY":
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and mouse_over:
                    if self.player_owns_group() and self.property.rent_idx <= 5 and self.would_be_even():
                        # Player is able and chooses to buy a house if enough money
                        if self.scene.players[self.scene.player_turn]["game_agent"].bank_balance >= self.house_price:
                            self.scene.players[self.scene.player_turn]["game_agent"].bank_balance  -= self.house_price
                            self.property.upgrade()
            if mouse_over and self.player_owns_group() and self.property.rent_idx <= 4 and self.would_be_even():
                self.show_house_prompt = True
            else:
                self.show_house_prompt = False
        elif self.space_type == "JACKPOT":
            if mouse_over:
                self.show_jackpot = True
            else:
                self.show_jackpot = False
    
    def get_coordinates(self):
        """Returns (
            (x1, y1) -> top left,
            (x2, y2) -> bottom right,
            (mx, my) -> midpoint
        )"""
        return (self.rect.topleft, self.rect.bottomright, self.rect.center)

    def set_next_space(self, next_space):
        self.next_space = next_space

    def get_next_space(self):
        return self.next_space
    
    def render(self, screen):
        # Get space color
        with open("ui/colors.json", 'r') as file:
            colors = json.load(file)
        color_rgb = colors[self.color] if not self.show_house_prompt else colors["WHITE"]
        if self.show_jackpot:
            color_rgb = colors["WHITE"]

        # Draw top rectangle
        if self.space_type == "PROPERTY" and not self.show_house_prompt:
            top_rect = (self.rect.topleft[0], self.rect.topleft[1], self.rect.width, self.rect.height // 3)
        else:
            top_rect = self.rect
        pygame.draw.rect(
            screen,
            color_rgb,
            top_rect
        )

        # Draw border outline
        pygame.draw.rect(
            screen,
            (0, 0, 0),  # Black color
            self.rect,
            2  # Outline thickness
        )

        # Draw top border outline 2 if property
        if self.space_type == "PROPERTY" and not self.show_house_prompt:
            pygame.draw.rect(
                screen,
                (0, 0, 0),  # Black color
                top_rect,
                1  # Outline thickness
            )
            
        # Write the center of self.rect
        if self.show_house_prompt:
            font = pygame.font.Font(None, 13 * self.camera_scale)
            if self.property.rent_idx < 4:
                text_surface = font.render(f"+HOUSE: £{self.house_price}", True, (0, 0, 0))
            else:
                text_surface = font.render(f"+HOTEL: £{self.house_price}", True, (0, 0, 0))
        elif self.show_jackpot:
            font = pygame.font.Font(None, 13 * self.camera_scale)
            text_surface = font.render(f"£{self.scene.jackpot}", True, (0, 0, 0))
        else:
            font = pygame.font.Font(None, 10 * self.camera_scale)
            text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

        # Write price if property
        if self.space_type == "PROPERTY" and not self.show_house_prompt:
            text_surface = font.render(f"£{self.property.get_value()}", True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=self.rect.center)
            scale_pos = 0.7     # set this to whatever scalar 0-1
            screen.blit(text_surface, (text_rect.topleft[0],
                                       text_rect.topleft[1] + (self.rect.height // 2) * scale_pos, # ensures not written outside space
                                       text_rect.width, text_rect.height))
            # draw any houses
            base_padding = (self.rect.width // 7) / 2
            square_len = self.rect.width // 6
            padding_coeff = 1
            square_coeff = 0
            if self.property.rent_idx <= 4:
                for _ in range(self.property.rent_idx): # draw houses
                    pygame.draw.rect(
                        screen,
                        colors["GREEN"],
                        (self.rect.topleft[0] + padding_coeff * base_padding + square_coeff * square_len, self.rect.topleft[1] + base_padding, square_len, square_len)
                    )
                    pygame.draw.rect(
                        screen,
                        (0,0,0),
                        (self.rect.topleft[0] + padding_coeff * base_padding + square_coeff * square_len, self.rect.topleft[1] + base_padding, square_len, square_len),
                        1
                    )
                    padding_coeff += 1
                    square_coeff += 1
            elif self.property.rent_idx > 4: # draw hotel
                pygame.draw.rect(
                    screen,
                    colors["RED"],
                    (self.rect.topleft[0] + base_padding, self.rect.topleft[1] + base_padding, square_len, square_len)
                )
                pygame.draw.rect(
                    screen,
                    (0,0,0),
                    (self.rect.topleft[0] + base_padding, self.rect.topleft[1] + base_padding, square_len, square_len),
                    1
                )

class LinkedSpaceList:
    def __init__(self):
        self.head_space = None

    def set_head_space(self, space):
        self.head_space = space

    def get_head_space(self):
        return self.head_space
