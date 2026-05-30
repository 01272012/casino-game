import pygame
import random
from ui import Button, TextInput

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
RED = (220, 20, 60)
GREEN = (0, 128, 0)
BLUE = (70, 130, 180)

class Symbol:
    """Represents a slot symbol."""
    symbols = ['🍒', '🍊', '🍋', '🍇', '🔔', '💎']
    symbol_names = ['Cherry', 'Orange', 'Lemon', 'Grape', 'Bell', 'Diamond']
    
    @staticmethod
    def get_random():
        return random.choice(Symbol.symbols)

class Reel:
    """Represents one reel in the slot machine."""
    def __init__(self, x, y, width=100, height=150):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.symbols = [Symbol.get_random() for _ in range(3)]  # Current 3 visible symbols
        self.spin_offset = 0  # Animation offset
        self.is_spinning = False
        self.spin_speed = 0
    
    def spin(self):
        """Start spinning this reel."""
        self.is_spinning = True
        self.spin_speed = random.randint(15, 25)  # Random speed
    
    def update(self):
        """Update reel animation."""
        if self.is_spinning:
            self.spin_offset += self.spin_speed
            
            # When spin_offset exceeds reel height, generate new symbol
            if self.spin_offset >= self.height:
                self.spin_offset = 0
                self.symbols.pop(0)
                self.symbols.append(Symbol.get_random())
            
            # Slow down near the end
            self.spin_speed *= 0.98
            if self.spin_speed < 1:
                self.is_spinning = False
                self.spin_offset = 0
    
    def draw(self, surface, font_small):
        """Draw the reel on the surface."""
        # Draw reel background
        pygame.draw.rect(surface, BLUE, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, GOLD, (self.x, self.y, self.width, self.height), 3)
        
        # Draw the 3 visible symbols with spinning animation
        for i in range(3):
            y_pos = self.y + (i * self.height // 3) - self.spin_offset
            text = font_small.render(self.symbols[i], True, WHITE)
            surface.blit(text, (self.x + self.width // 2 - 20, y_pos + 30))
    
    def get_middle_symbol(self):
        """Get the symbol in the middle (winning line)."""
        return self.symbols[1]

class SlotsGame:
    def __init__(self, player, width, height):
        self.player = player
        self.width = width
        self.height = height
        
        self.state = "BETTING"  # BETTING, SPINNING, RESULT
        self.bet_amount = 0
        self.result_message = ""
        self.winnings = 0
        
        # Fonts
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 36)
        
        # UI
        self.bet_input = TextInput(self.width // 2 - 100, 250, 200)
        self.buttons = {
            "PLACE_BET": Button(self.width // 2 - 75, 320, 150, 50, "Spin\nfor $", 24),
            "SPIN": Button(self.width // 2 - 75, 500, 150, 50, "SPIN!", 28),
            "PLAY_AGAIN": Button(self.width // 2 - 75, 500, 150, 50, "Play Again", 24),
            "BACK": Button(20, 20, 100, 40, "Back", 20),
        }
        
        # Create 3 reels
        reel_spacing = 40
        reel_width = 100
        reel_height = 150
        first_reel_x = (self.width - (3 * reel_width + 2 * reel_spacing)) // 2
        
        self.reels = [
            Reel(first_reel_x, 200, reel_width, reel_height),
            Reel(first_reel_x + reel_width + reel_spacing, 200, reel_width, reel_height),
            Reel(first_reel_x + 2 * (reel_width + reel_spacing), 200, reel_width, reel_height),
        ]
        
        self.player.play_game("slots")
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.buttons["BACK"].is_clicked(event.pos):
                return "BACK_TO_MENU"
            
            if self.state == "BETTING":
                if self.buttons["PLACE_BET"].is_clicked(event.pos):
                    bet = self.bet_input.get_value()
                    if 0 < bet <= self.player.money:
                        self.bet_amount = bet
                        self.player.bet(bet)
                        self.start_spin()
                        self.state = "SPINNING"
            
            elif self.state == "RESULT":
                if self.buttons["PLAY_AGAIN"].is_clicked(event.pos):
                    self.reset_game()
        
        if self.state == "BETTING":
            self.bet_input.handle_event(event)
    
    def start_spin(self):
        """Start all reels spinning."""
        for reel in self.reels:
            reel.spin()
    
    def check_win(self):
        """Check if the player won and calculate winnings."""
        symbols = [reel.get_middle_symbol() for reel in self.reels]
        
        # All three match - jackpot
        if symbols[0] == symbols[1] == symbols[2]:
            multiplier = 10  # 10x payout for 3 of a kind
            self.winnings = self.bet_amount * multiplier
            self.player.win(self.winnings + self.bet_amount, "slots")  # +bet because they keep their bet
            self.result_message = f"JACKPOT! {symbols[0]} {symbols[0]} {symbols[0]} | You win ${self.winnings}!"
            return True
        
        # Two match
        elif symbols[0] == symbols[1] or symbols[1] == symbols[2] or symbols[0] == symbols[2]:
            multiplier = 2  # 2x payout for 2 of a kind
            self.winnings = self.bet_amount * multiplier
            self.player.win(self.winnings + self.bet_amount, "slots")
            matching_symbol = symbols[0] if symbols[0] == symbols[1] else symbols[1]
            self.result_message = f"Nice! 2 matching symbols | You win ${self.winnings}!"
            return True
        
        # No match - loss
        else:
            self.result_message = f"No match. Better luck next time!"
            return False
    
    def update(self):
        if self.state == "SPINNING":
            # Update all reels
            all_stopped = True
            for reel in self.reels:
                reel.update()
                if reel.is_spinning:
                    all_stopped = False
            
            # Check win when all reels have stopped
            if all_stopped:
                self.check_win()
                self.state = "RESULT"
    
    def draw(self, surface, current_money):
        # Draw title
        title = self.font_large.render("SLOTS", True, GOLD)
        surface.blit(title, (self.width // 2 - 100, 20))
        
        # Draw money
        money_text = self.font_small.render(f"Balance: ${current_money:,.2f}", True, WHITE)
        surface.blit(money_text, (20, 60))
        
        # Draw back button
        self.buttons["BACK"].draw(surface)
        
        if self.state == "BETTING":
            prompt = self.font_medium.render("Enter bet amount:", True, WHITE)
            surface.blit(prompt, (self.width // 2 - 150, 200))
            self.bet_input.draw(surface)
            self.buttons["PLACE_BET"].draw(surface)
        
        elif self.state in ["SPINNING", "RESULT"]:
            # Draw reels
            for reel in self.reels:
                reel.draw(surface, self.font_small)
            
            if self.state == "RESULT":
                # Draw result
                result_text = self.font_large.render(self.result_message, True, GOLD)
                surface.blit(result_text, (self.width // 2 - 300, 400))
                self.buttons["PLAY_AGAIN"].draw(surface)
    
    def reset_game(self):
        """Reset for next game."""
        self.state = "BETTING"
        self.bet_input.text = ""
        self.bet_amount = 0
        self.result_message = ""
        self.winnings = 0
        
        # Reset reels with new random symbols
        for reel in self.reels:
            reel.symbols = [Symbol.get_random() for _ in range(3)]
            reel.spin_offset = 0
            reel.is_spinning = False
