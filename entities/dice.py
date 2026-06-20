import pygame
import random
import time
from entities.animated_entity import AnimatedEntity

class Dice(AnimatedEntity):
    def __init__(self, x, y):
        # List of dice face images (indexed 0-5)
        dice_faces = [
            "assets/dice_1.png",
            "assets/dice_2.png",
            "assets/dice_3.png",
            "assets/dice_4.png",
            "assets/dice_5.png",
            "assets/dice_6.png"
        ]

        super().__init__(x, y, 60, 60, dice_faces, frame_duration=0.05, random_shuffle=True)

        self.final_value = random.randint(1, 6)  # The final dice roll (1-6)
        self.called_end_roll = True
        self.after_roll_callback = None

        # NEW: cooldown variables
        self.cooldown_duration = 0.5  # half-second delay before callback
        self.cooldown_active = False
        self.stop_time = 0

        # Sound effect
        self.sound = pygame.mixer.Sound("assets/audio/sounds/dice_roll.wav")
        self.sound.set_volume(0.25)

    def roll(self, after_roll_callback=None, sound=False):
        """Starts the rolling animation for 1 second and determines final dice value."""
        if sound:
            pygame.mixer.Sound.play(self.sound, loops=-1)
        self.after_roll_callback = after_roll_callback
        if not self.animating:  # Prevent double clicks
            self.final_value = random.randint(1, 6)  # Get a dice value (1-6)
            self.start_animation(loop=True, duration=1.0)  # Animate for 1 second
        return self.final_value

    def update(self):
        """After animation duration, display the final dice face and wait cooldown before callback."""
        super().update()  # Handle frame updates (random shuffle, time check, etc.)

        # If just started animating, reset 'called_end_roll'
        if self.animating and self.called_end_roll:
            self.called_end_roll = False

        # If animation has ended but we haven't set the final face yet
        if not self.animating and not self.called_end_roll:
            self.called_end_roll = True
            self.current_frame = self.final_value - 1  # set final face

            # Start cooldown timer: do NOT call callback yet
            self.cooldown_active = True
            self.stop_time = time.time()
            pygame.mixer.Sound.stop(self.sound)

        # Check if we're in cooldown mode
        if self.cooldown_active:
            now = time.time()
            if now - self.stop_time >= self.cooldown_duration:
                # Enough time has passed, call callback if present
                self.cooldown_active = False
                if self.after_roll_callback:
                    self.after_roll_callback()
