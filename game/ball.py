import pygame
from game.brick import Brick


class Ball:
    """
    Represents a ball in the Breakout game.
    Handles movement, wall collisions, and paddle/brick interactions.
    """

    def __init__(self, x, y, width, height, speed, acceleration=0, simulated=False):
        # Create ball rectangle and movement attributes
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.accel = acceleration
        self.dx = 1
        self.dy = -1
        self.prev_x = x
        self.prev_y = y
        self.simulated = simulated # simulated=True is used for power-up generated balls

    def move(self):
        """Move the ball and store previous position for collision detection."""
        # Store previous position for collision side detection
        self.prev_x = self.rect.x
        self.prev_y = self.rect.y

        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed

    def update(self, screen_width, obj):
        """Handle wall collisions and paddle collisions (brick collisions handled externally)."""
        if self.rect.left < 0:
            self.rect.left = 0
            self.dx *= -1

        if self.rect.right > screen_width:
            self.rect.right = screen_width
            self.dx *= -1

        if self.rect.top < 0:
            self.rect.top = 0
            self.dy *= -1

        if self.rect.colliderect(obj.rect):
            if isinstance(obj, Brick):
                self.handle_brick_collision(obj)
            else:
                self.dy *= -1
                # Increase speed only when hitting paddle (optional acceleration feature)
                self.speed += self.accel

    def handle_brick_collision(self, brick):
        """Invert ball direction based on which side of the brick was hit."""

        if self.prev_y + self.rect.height <= brick.rect.top:
            self.dy *= -1

        elif self.prev_y >= brick.rect.bottom:
            self.dy *= -1

        elif self.prev_x + self.rect.width <= brick.rect.left:
            self.dx *= -1

        elif self.prev_x >= brick.rect.right:
            self.dx *= -1

    def draw(self, surface, color):
        """Render ball on screen."""
        pygame.draw.circle(surface, color, self.rect.center, self.rect.width // 2)

