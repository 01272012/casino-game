import pygame
import random
import math
from ui import Button, TextInput

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
RED = (220, 20, 60)
GREEN = (0, 128, 0)
BLUE = (70, 130, 180)
DARK_RED = (139, 0, 0)
DARK_GREEN = (0, 100, 0)

class RouletteWheel:
    """Represents the roulette wheel."""
    def __init__(self, cx, cy, radius):
        self.cx = cx
        self.cy = cy
        self.radius = radius
        self.rotation = 0  # Current rotation angle
        self.is_spinning = False
        self.spin_speed = 0
        
        # Standard roulette: 0-36 (37 numbers)
        # Red: 1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36
        # Black: 2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35
        # Green: 0
        
        self.numbers = list(range(37))
        self.red_numbers = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
        self.black_numbers = [2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35]
        self.green_numbers = [0]
        
        # Calculate angle for each number
        self.angle_per_slot = 360 / 37
    
    def spin(self):
        """Start spinning the wheel."""
        self.is_spinning = True
        self.spin_speed = random.uniform(15, 25)  # Random speed
    
    def update(self):
        """Update wheel rotation."""
        if self.is_spinning:
            self.rotation += self.spin_speed
            self.rotation %= 360
            
            # Slow down
            self.spin_speed *= 0.98
            if self.spin_speed < 0.5:
                self.is_spinning = False
    
    def get_winning_number(self):
        """Get the number at the top (12 o'clock position)."""
        # Adjust rotation so 0 is at top
        adjusted_rotation = (self.rotation + 90) % 360
        slot = int(adjusted_rotation / self.angle_per_slot) % 37
        return self.numbers[slot]
    
    def get_number_color(self, number):
        """Return color of a number."""
        if number in self.red_numbers:
            return "RED"
        elif number in self.black_numbers:
            return "BLACK"
        else:
            return "GREEN"
    
    def draw(self, surface, font):
        """Draw the roulette wheel."""
        # Draw wheel background
        pygame.draw.circle(surface, GOLD, (self.cx, self.cy), self.radius + 10, 3)
        
        # Draw wheel slots
        for i in range(37):
            angle = (i * self.angle_per_slot + self.rotation) * math.pi / 180
            number = self.numbers[i]
            
            # Determine color
            if number in self.red_numbers:
                slot_color = RED
            elif number in self.black_numbers:
                slot_color = BLACK
            else:
                slot_color = GREEN
            
            # Calculate slot position
            start_angle = angle
            end_angle = angle + (self.angle_per_slot * math.pi / 180)
            
            # Draw pie slice for this number
            pygame.draw.polygon(surface, slot_color, [
                (self.cx, self.cy),
                (self.cx + self.radius * math.cos(start_angle), 
                 self.cy + self.radius * math.sin(start_angle)),
                (self.cx + (self.radius - 20) * math.cos(start_angle + (end_angle - start_angle) / 2),
                 self.cy + (self.radius - 20) * math.sin(start_angle + (end_angle - start_angle) / 2)),
            ])
            
            # Draw number text on wheel
            mid_angle = start_angle + (end_angle - start_angle) / 2
            text_x = self.cx + (self.radius - 35) * math.cos(mid_angle)
            text_y = self.cy + (self.radius - 35) * math.sin(mid_angle)
            
            text = font.render(str(number), True, WHITE)
            text_rect = text.get_rect(center=(text_x, text_y))
            surface.blit(text, text_rect)
        
        # Draw pointer at top
        pointer_points = [
            (self.cx, self.cy - self.radius - 15),
            (self.cx - 15, self.cy - self.radius + 5),
            (self.cx + 15, self.cy - self.radius + 5)
        ]
        pygame.draw.polygon(surface, GOLD, pointer_points)

class RouletteGame:
    def __init__(self, player, width, height):
        self.player = player
        self.width = width
        self.height = height
        
        self.state = "BETTING"  # BETTING, SPINNING, RESULT
        self.bet_type = None  # "RED", "BLACK", "GREEN", or number (0-36)
        self.bet_amount = 0
        self.result_message = ""
        self.winning_number = None
        
        # Fonts
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 28)
        self.font_small = pygame.font.Font(None, 20)
        
        # Create wheel
        self.wheel = RouletteWheel(width // 2, 200, 120)
        
        # UI
        self.bet_input = TextInput(self.width // 2 - 75, 450, 150)
        
        self.buttons = {
            "RED": Button(100, 450, 100, 50, "Red", 24),
            "BLACK": Button(220, 450, 100, 50, "Black", 24),
            "GREEN": Button(340, 450, 100, 50, "Green", 24),
            "NUMBER": Button(460, 450, 120, 50, "Number (0-36)", 18),
            "SPIN": Button(self.width // 2 - 75, 530, 150, 50, "SPIN!", 28),
            "PLAY_AGAIN": Button(self.width // 2 - 75, 550, 150, 50, "Play Again", 24),
            "BACK": Button(20, 20, 100, 40, "Back", 20),
        }
        
        self.selected_bet = None  # To show which bet is selected
        self.player.play_game("roulette")
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.buttons["BACK"].is_clicked(event.pos):
                return "BACK_TO_MENU"
            
            if self.state == "BETTING":
                if self.buttons["RED"].is_clicked(event.pos):
                    self.selected_bet = "RED"
                    self.bet_type = "RED"
                elif self.buttons["BLACK"].is_clicked(event.pos):
                    self.selected_bet = "BLACK"
                    self.bet_type = "BLACK"
                elif self.buttons["GREEN"].is_clicked(event.pos):
                    self.selected_bet = "GREEN"
                    self.bet_type = "GREEN"
                elif self.buttons["NUMBER"].is_clicked(event.pos):
                    self.selected_bet = "NUMBER"
                
                elif self.buttons["SPIN"].is_clicked(event.pos):
                    if self.bet_type and self.bet_amount > 0:
                        self.player.bet(self.bet_amount)
                        self.start_spin()
                        self.state = "SPINNING"
            
            elif self.state == "RESULT":
                if self.buttons["PLAY_AGAIN"].is_clicked(event.pos):
                    self.reset_game()
        
        if self.state == "BETTING" and self.selected_bet == "NUMBER":
            self.bet_input.handle_event(event)
    
    def start_spin(self):
        """Start the wheel spinning."""
        self.wheel.spin()
    
    def check_win(self):
        """Check if the player won."""
        self.winning_number = self.wheel.get_winning_number()
        winning_color = self.wheel.get_number_color(self.winning_number)
        
        # Determine payout multiplier
        payout_multiplier = 0
        
        if self.bet_type == "RED" and winning_color == "RED":
            payout_multiplier = 2
            self.result_message = f"RED wins! {self.winning_number} is RED. You win ${self.bet_amount * payout_multiplier}!"
        elif self.bet_type == "BLACK" and winning_color == "BLACK":
            payout_multiplier = 2
            self.result_message = f"BLACK wins! {self.winning_number} is BLACK. You win ${self.bet_amount * payout_multiplier}!"
        elif self.bet_type == "GREEN" and winning_color == "GREEN":
            payout_multiplier = 36  # Green pays 36:1
            self.result_message = f"GREEN wins! You hit 0! You win ${self.bet_amount * payout_multiplier}!"
        elif isinstance(self.bet_type, int) and self.bet_type == self.winning_number:
            payout_multiplier = 36  # Straight number pays 36:1
            self.result_message = f"You hit {self.winning_number}! You win ${self.bet_amount * payout_multiplier}!"
        else:
            self.result_message = f"The wheel landed on {self.winning_number} ({winning_color}). You lose."
        
        if payout_multiplier > 0:
            self.player.win(self.bet_amount * payout_multiplier + self.bet_amount, "roulette")
    
    def update(self):
        self.wheel.update()
        
        if self.state == "SPINNING" and not self.wheel.is_spinning:
            self.check_win()
            self.state = "RESULT"
    
    def draw(self, surface, current_money):
        # Draw title
        title = self.font_large.render("ROULETTE", True, GOLD)
        surface.blit(title, (self.width // 2 - 150, 20))
        
        # Draw money
        money_text = self.font_small.render(f"Balance: ${current_money:,.2f}", True, WHITE)
        surface.blit(money_text, (20, 60))
        
        # Draw wheel
        self.wheel.draw(surface, self.font_small)
        
        # Draw back button
        self.buttons["BACK"].draw(surface)
        
        if self.state == "BETTING":
            # Draw betting options
            self.buttons["RED"].draw(surface)
            self.buttons["BLACK"].draw(surface)
            self.buttons["GREEN"].draw(surface)
            self.buttons["NUMBER"].draw(surface)
            
            # Draw selected bet
            if self.selected_bet:
                selected_text = self.font_medium.render(f"Selected: {self.selected_bet}", True, GOLD)
                surface.blit(selected_text, (self.width // 2 - 100, 380))
            
            # Draw bet amount input
            bet_label = self.font_medium.render("Bet Amount:", True, WHITE)
            surface.blit(bet_label, (self.width // 2 - 150, 420))
            self.bet_input.draw(surface)
            
            # Get bet amount from input
            if self.bet_input.get_value() > 0:
                self.bet_amount = self.bet_input.get_value()
            
            # Handle number input
            if self.selected_bet == "NUMBER":
                num_text = self.font_small.render("Enter number (0-36):", True, WHITE)
                surface.blit(num_text, (450, 420))
                try:
                    num = int(self.bet_input.text.split(',')[0]) if ',' not in self.bet_input.text else 0
                    if 0 <= num <= 36:
                        self.bet_type = num
                except:
                    pass
            
            self.buttons["SPIN"].draw(surface)
        
        elif self.state == "SPINNING":
            spin_text = self.font_medium.render("Spinning...", True, GOLD)
            surface.blit(spin_text, (self.width // 2 - 100, 350))
        
        elif self.state == "RESULT":
            # Draw result
            result_text = self.font_large.render(self.result_message, True, GOLD)
            surface.blit(result_text, (self.width // 2 - 300, 350))
            
            # Draw winning number
            if self.winning_number is not None:
                win_num_text = self.font_medium.render(f"Winning Number: {self.winning_number}", True, WHITE)
                surface.blit(win_num_text, (self.width // 2 - 150, 420))
            
            self.buttons["PLAY_AGAIN"].draw(surface)
    
    def reset_game(self):
        """Reset for next game."""
        self.state = "BETTING"
        self.bet_type = None
        self.bet_amount = 0
        self.result_message = ""
        self.winning_number = None
        self.selected_bet = None
        self.bet_input.text = ""
        self.wheel.rotation = 0
