import pygame
import random
from ui import Button

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)

class HorseRacingGame:
    def __init__(self, player, width, height):
        self.player = player
        self.width = width
        self.height = height
        self.state = "BETTING"
        self.message = "Horse Racing - Coming soon"
        self.player.play_game("horse_racing")
    
    def handle_event(self, event):
        pass
    
    def update(self):
        pass
    
    def draw(self, surface, current_money):
        font = pygame.font.Font(None, 48)
        text = font.render(self.message, True, GOLD)
        surface.blit(text, (self.width // 2 - 200, self.height // 2))
