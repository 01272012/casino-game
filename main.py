import pygame
import sys
from player import Player
from ui import Menu
from games.blackjack import BlackjackGame
from games.slots import SlotsGame
from games.roulette import RouletteGame
from games.horse_racing import HorseRacingGame
from games.pool import PoolGame

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1000, 700
FPS = 60

# Colors
BG_COLOR = (34, 139, 34)  # Dark green (casino felt)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)

class CasinoGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Casino Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_state = "MENU"
        
        # Game state
        self.player = Player(start_money=1000)
        self.menu = Menu(WIDTH, HEIGHT)
        self.current_game = None
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if self.current_state == "MENU":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    choice = self.menu.handle_click(event.pos)
                    if choice == "BLACKJACK":
                        self.current_game = BlackjackGame(self.player, WIDTH, HEIGHT)
                        self.current_state = "PLAYING"
                    elif choice == "SLOTS":
                        self.current_game = SlotsGame(self.player, WIDTH, HEIGHT)
                        self.current_state = "PLAYING"
                    elif choice == "ROULETTE":
                        self.current_game = RouletteGame(self.player, WIDTH, HEIGHT)
                        self.current_state = "PLAYING"
                    elif choice == "POOL":
                        self.current_game = PoolGame(self.player, WIDTH, HEIGHT)
                        self.current_state = "PLAYING"
                    elif choice == "HORSE_RACING":
                        self.current_game = HorseRacingGame(self.player, WIDTH, HEIGHT)
                        self.current_state = "PLAYING"
                    elif choice == "QUIT":
                        self.running = False
            
            elif self.current_state == "PLAYING":
                result = self.current_game.handle_event(event)
                if result == "BACK_TO_MENU":
                    self.current_state = "MENU"
                    self.current_game = None
    
    def update(self):
        if self.current_state == "PLAYING" and self.current_game:
            self.current_game.update()
    
    def draw(self):
        self.screen.fill(BG_COLOR)
        
        if self.current_state == "MENU":
            self.menu.draw(self.screen, self.player.money, self.player.total_wins)
        elif self.current_state == "PLAYING" and self.current_game:
            self.current_game.draw(self.screen, self.player.money)
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = CasinoGame()
    game.run()
