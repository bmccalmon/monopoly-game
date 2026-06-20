import pygame
import time
from entities.entity import Entity
from corporation import Corporation

class GameAgent(Entity, Corporation):
    def __init__(self, name, starting_space, token_path):
        self.current_space = starting_space
        starting_pos = starting_space.get_coordinates()
        # override_offsets = True ensures camera transforms are ignored
        Entity.__init__(self, starting_pos[0][0], starting_pos[0][1], 60, 60, override_offsets=True)
        Corporation.__init__(self, name)

        # jail info
        self.remaining_sentence = 0

        # Load player token image
        self.token = pygame.image.load(token_path)

        # Movement animation variables
        self.moving = False
        self.move_path = []  # List of spaces to jump through
        self.move_delay = 200  # Time in ms between jumps
        self.last_move_time = 0  # Track time between jumps

        # NEW: Cooldown variables
        self.cooldown_duration = 500  # in milliseconds
        self.cooldown_active = False
        self.stop_time = 0  # track when final move ended

        # Sound effects
        self.sound = pygame.mixer.Sound("assets/audio/sounds/piece_move.wav")
        self.sound.set_volume(0.5)

    def get_current_space(self):
        # If "moving" is True or cooldown is still active, return final destination
        if self.moving or self.cooldown_active:
            return self.move_path[-1] if self.move_path else self.current_space
        return self.current_space

    def set_current_space(self, space):
        self.current_space = space

        # Sound effect
        pygame.mixer.Sound.play(self.sound)

    def jump_spaces(self, num=1):
        self.move_path = []
        next_space = self.current_space
        
        for _ in range(num):
            next_space = next_space.next_space
            self.move_path.append(next_space)
        
        self.moving = True
        self.cooldown_active = False  # reset any previous cooldown
        self.last_move_time = pygame.time.get_ticks()
        return self.get_current_space()
    
    def go_to_jail(self):
        curr_space = self.current_space.next_space
        while curr_space != self.current_space:
            if curr_space.text == "JAIL":
                target_space = curr_space
                break
            curr_space = curr_space.next_space
        self.set_current_space(target_space)
        self.remaining_sentence = 2

    def update(self):
        now = pygame.time.get_ticks()

        # If we are currently moving along the path:
        if self.moving and self.move_path:
            if now - self.last_move_time >= self.move_delay:
                # Move to the next space
                next_space = self.move_path.pop(0)
                self.set_current_space(next_space)
                self.last_move_time = now

            # If finished moving, trigger the cooldown
            if not self.move_path:
                self.cooldown_active = True
                self.stop_time = now
                # Don't set self.moving to False yet -- we wait until cooldown

        # If cooldown is active, check if it's over
        if self.cooldown_active:
            if now - self.stop_time >= self.cooldown_duration:
                self.cooldown_active = False
                self.moving = False  # Officially end movement

    def render(self, screen):
        """Draw the player's token at the center of current space."""
        pos = self.current_space.get_coordinates()
        super().set_pos(pos[2][0], pos[2][1])
        self.token = pygame.transform.scale(self.token, (self.rect.width, self.rect.height))
        screen.blit(self.token, self.rect)
