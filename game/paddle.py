import pygame

class Paddle:
    """Player-controlled paddle that moves horizontally at the bottom of the screen."""

    def __init__(self, x, y, width, height, speed):
        # Create paddle rectangle and movement attributes
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.direction = 0

    def handle_input(self):
        """Read keyboard input and set movement direction"""
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
            self.direction = 0
        elif keys[pygame.K_LEFT]:
            self.direction = -1
        elif keys[pygame.K_RIGHT]:
            self.direction = 1
        else:
            self.direction = 0

    def update(self, screen_width):
        # Move paddle and clamp it inside screen boundaries
        self.rect.x += self.direction * self.speed

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width

    def draw(self, surface, color):
        """Render paddle on screen"""
        pygame.draw.rect(surface, color, self.rect)
