import pygame

class Entity:
    def __init__(self, x, y, width, height, centered=True, override_offsets=False):
        self.original_x = x
        self.original_y = y
        self.original_width = width
        self.original_height = height
        self.centered = centered

        self.override_offets = override_offsets
        self.camera_offset = pygame.Vector2(0, 0)
        self.camera_scale = 1.0

        self.rect = pygame.Rect(0, 0, width, height)
        self.update_rect()

    def set_pos(self, x, y, centered=True):
        self.original_x = x
        self.original_y = y
        self.centered = centered
        self.update_rect()

    def set_camera(self, offset_x, offset_y, scale):
        self.camera_offset = pygame.Vector2(offset_x, offset_y)
        self.camera_scale = scale
        self.update_rect()

    def update_rect(self):
        x = self.original_x
        y = self.original_y
        w = self.original_width
        h = self.original_height

        if self.centered:
            x -= w // 2
            y -= h // 2

        # Apply camera offset and scale
        if not self.override_offets:
            x = (x + self.camera_offset.x) * self.camera_scale
            y = (y + self.camera_offset.y) * self.camera_scale
            w *= self.camera_scale
            h *= self.camera_scale

        self.rect = pygame.Rect(x, y, w, h)

    def handle_events(self, events):
        """Override this method to handle events (e.g., clicks, keyboard input)."""
        pass

    def update(self):
        """Override this method for updates (e.g., movement, animations)."""
        pass

    def render(self, screen):
        pass
