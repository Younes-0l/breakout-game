import pygame, random
from game import settings


class Brick:
    """
    Represents a destructible brick in the Breakout game.
    Handles durability, color transitions, item drops, and rendering.
    """

    def __init__(self, x, y, width, height, type_):
        # Initialize brick properties including durability and color states
        self.rect = pygame.Rect(x, y, width, height)
        self.type = type_
        self.name = type_['name']
        self.resistance = type_['resistance']
        self.score = type_['score']
        self.color = type_['base_color']
        self.alive = True

    def change_color(self):
        # Update brick color based on remaining resistance
        if self.resistance == 2:
            self.color = self.type['cracked_color']
        elif self.resistance == 1:
            self.color = self.type['damaged_color']
        
    def get_chance(self):
        # Return drop chance based on brick type
        if self.name == "weak":
            chance = 0.1
        elif self.name == "ordinary":
            chance = 0.3
        elif self.name == "hard":
            chance = 0.5
        return chance
    
    def get_item(self, chance, items: list):
        # Randomly return an item or None based on drop chance
        result = []
        empty = int((1 - chance) * 10)
        for _ in range(empty):
            result.append(None)
        while len(result) < 10:
            result.append(random.choice(items))
        return random.choice(result)

    def destroy(self):
        """Mark brick as destroyed and return dropped item (if any)"""
        self.alive = False
        chance = self.get_chance()
        item = self.get_item(chance, settings.BASIC_ITEMS)
        return item

    def drop_item(self):
        """
        Destroy brick if resistance is zero and return dropped item.
        Returns:
            - item name (str) if dropped
            - True if destroyed but no item
            - False if still alive
        """
        if self.resistance <= 0:
            item = self.destroy()
            return item if item is not None else True
        return False
    
    def take_damage(self):
        self.resistance -= 1
        self.change_color()

    def draw(self, surface):
        """Render brick on screen"""
        pygame.draw.rect(surface, self.color, self.rect)
        