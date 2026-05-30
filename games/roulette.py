import pygame
import random
from ui import Button

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)

class RouletteGame:
    def __init__(self, player, width, height):
        self.player = player
        self.width = width
        self.height = height
        self.state = "BETTING"
        self.message = "Roulette - Coming soon"
        self.player.play_game("roulette")
    
    def handle_event(self, event):
        pass
    
    def update(self):
        pass
    
    def draw(self, surface, current_money):
        font = pygame.font.Font(None, 48)
        text = font.render(self.message, True, GOLD)
        surface.blit(text, (self.width // 2 - 200, self.height // 2))
