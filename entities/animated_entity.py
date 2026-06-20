import pygame
import time
import random
from entities.entity import Entity

class AnimatedEntity(Entity):
    def __init__(
        self,
        x,
        y,
        width,
        height,
        image_paths,
        frame_duration=0.1,
        animation_duration=None,
        loop=False,
        random_shuffle=False  # NEW: Whether to randomize frames
    ):
        """
        A base class for entities that need animations.

        :param x, y: Position of entity.
        :param width, height: Size of entity.
        :param image_paths: List of image file paths.
        :param frame_duration: Time per frame in seconds.
        :param animation_duration: Total time the animation runs (None = infinite).
        :param loop: Should the animation loop in sequential mode?
        :param random_shuffle: If True, frames are picked at random each update.
        """
        super().__init__(x, y, width, height)
        self.images = [pygame.image.load(path) for path in image_paths]  # Load all images
        self.images = [pygame.transform.scale(img, (width, height)) for img in self.images]  # Resize images

        self.current_frame = 0
        self.frame_duration = frame_duration  # Time per frame
        self.animation_duration = animation_duration  # How long the animation runs
        self.loop = loop
        self.random_shuffle = random_shuffle  # NEW: store the shuffle mode

        self.animating = False
        self.start_time = None  # Track when animation started
        self.last_update_time = time.time()

    def start_animation(self, loop=False, duration=None):
        """Start the animation with optional looping and duration."""
        self.animating = True
        self.loop = loop
        self.animation_duration = duration
        self.current_frame = 0
        self.start_time = time.time()  # Mark animation start
        self.last_update_time = self.start_time

    def stop_animation(self):
        """Stop animation and reset to first frame."""
        self.animating = False
        self.current_frame = 0

    def update(self):
        """Handles animation updates based on time."""
        if self.animating:
            now = time.time()

            # Check if we've exceeded the total animation duration
            if self.animation_duration and (now - self.start_time >= self.animation_duration):
                self.animating = False
                return

            # Advance frames if enough time has passed
            if now - self.last_update_time > self.frame_duration:
                self.last_update_time = now

                # If we're in random shuffle mode:
                if self.random_shuffle:
                    # Pick a random frame each time
                    self.current_frame = random.randrange(len(self.images))
                else:
                    # Sequential mode
                    self.current_frame += 1
                    if self.current_frame >= len(self.images):
                        if self.loop:
                            self.current_frame = 0  # Loop animation
                        else:
                            self.stop_animation()  # Stop at last frame

    def render(self, screen):
        """Renders the current frame."""
        screen.blit(self.images[self.current_frame], self.rect)
