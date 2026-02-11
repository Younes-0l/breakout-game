import pygame


class PowerUp:
    """
    Represents a falling power-up item dropped from a brick.
    Handles movement, collision detection, and rendering.
    """

    def __init__(self, x, y, width, height, type_, speed, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.type = type_
        self.speed = speed
        self.color = color

    def move(self):
        self.rect.y += self.speed
    
    # def update(self, screen_height):        
    #     if self.rect.y > screen_height:
    #         del self

    def check_collision(self, obj):
        return self.rect.colliderect(obj.rect)

    
    def draw(self, surface):
        """Render item on screen"""
        pygame.draw.rect(surface, self.color, self.rect)