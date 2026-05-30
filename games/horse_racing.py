import pygame
import random
from ui import Button, TextInput

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
RED = (220, 20, 60)
GREEN = (0, 128, 0)
BLUE = (70, 130, 180)
GRAY = (128, 128, 128)

class Horse:
    """Represents a racing horse."""
    def __init__(self, horse_id, start_x, start_y, track_width):
        self.id = horse_id  # 1-4
        self.start_x = start_x
        self.start_y = start_y
        self.track_width = track_width
        self.x = start_x
        self.y = start_y
        
        # Racing stats
        self.speed = random.uniform(2, 4)  # Base speed varies per horse
        self.current_speed = 0
        self.stamina = 100
        self.finished = False
        self.finish_time = 0
        
        # Colors for each horse
        self.colors = [RED, GOLD, BLUE, GREEN]
        self.color = self.colors[horse_id - 1]
        
        # Horse names
        self.names = ["Thunder", "Lightning", "Storm", "Blaze"]
        self.name = self.names[horse_id - 1]
    
    def update(self, is_racing):
        """Update horse position during race."""
        if not self.finished and is_racing:
            # Vary speed slightly (momentum changes)
            self.current_speed = self.speed + random.uniform(-0.3, 0.3)
            
            # Stamina decreases over time
            self.stamina -= random.uniform(0.2, 0.5)
            self.stamina = max(0, self.stamina)
            
            # Speed affected by stamina
            stamina_factor = self.stamina / 100
            actual_speed = self.current_speed * stamina_factor
            
            self.x += actual_speed
            
            # Check if finished
            if self.x >= self.start_x + self.track_width:
                self.finished = True
                self.x = self.start_x + self.track_width
    
    def draw(self, surface, font):
        """Draw the horse."""
        # Draw horse body (simple rectangle with name)
        horse_width = 40
        horse_height = 20
        pygame.draw.rect(surface, self.color, (self.x, self.y, horse_width, horse_height))
        pygame.draw.rect(surface, GOLD, (self.x, self.y, horse_width, horse_height), 2)
        
        # Draw horse number
        num_text = font.render(str(self.id), True, WHITE)
        surface.blit(num_text, (self.x + 15, self.y + 2))
        
        # Draw stamina bar above horse
        stamina_width = 40
        stamina_height = 5
        pygame.draw.rect(surface, GRAY, (self.x, self.y - 10, stamina_width, stamina_height))
        pygame.draw.rect(surface, GREEN, (self.x, self.y - 10, stamina_width * (self.stamina / 100), stamina_height))
    
    def reset(self):
        """Reset horse for new race."""
        self.x = self.start_x
        self.y = self.start_y
        self.speed = random.uniform(2, 4)
        self.current_speed = 0
        self.stamina = 100
        self.finished = False
        self.finish_time = 0

class HorseRacingGame:
    def __init__(self, player, width, height):
        self.player = player
        self.width = width
        self.height = height
        
        self.state = "BETTING"  # BETTING, RACING, RESULT
        self.selected_horse = None
        self.bet_amount = 0
        self.result_message = ""
        self.winning_horse = None
        self.race_time = 0
        
        # Fonts
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 28)
        self.font_small = pygame.font.Font(None, 20)
        
        # Create 4 horses
        track_width = 600
        start_x = 200
        horses_start_y = [150, 220, 290, 360]
        
        self.horses = [
            Horse(1, start_x, horses_start_y[0], track_width),
            Horse(2, start_x, horses_start_y[1], track_width),
            Horse(3, start_x, horses_start_y[2], track_width),
            Horse(4, start_x, horses_start_y[3], track_width),
        ]
        
        self.track_start_x = start_x
        self.track_end_x = start_x + track_width
        
        # UI
        self.bet_input = TextInput(self.width // 2 - 75, 480, 150)
        
        self.buttons = {
            "HORSE_1": Button(50, 150, 120, 50, "Horse 1\nThunder", 18),
            "HORSE_2": Button(50, 220, 120, 50, "Horse 2\nLightning", 18),
            "HORSE_3": Button(50, 290, 120, 50, "Horse 3\nStorm", 18),
            "HORSE_4": Button(50, 360, 120, 50, "Horse 4\nBlaze", 18),
            "RACE": Button(self.width // 2 - 75, 530, 150, 50, "START RACE!", 28),
            "PLAY_AGAIN": Button(self.width // 2 - 75, 550, 150, 50, "Play Again", 24),
            "BACK": Button(20, 20, 100, 40, "Back", 20),
        }
        
        self.player.play_game("horse_racing")
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.buttons["BACK"].is_clicked(event.pos):
                return "BACK_TO_MENU"
            
            if self.state == "BETTING":
                # Select horse
                if self.buttons["HORSE_1"].is_clicked(event.pos):
                    self.selected_horse = 0
                elif self.buttons["HORSE_2"].is_clicked(event.pos):
                    self.selected_horse = 1
                elif self.buttons["HORSE_3"].is_clicked(event.pos):
                    self.selected_horse = 2
                elif self.buttons["HORSE_4"].is_clicked(event.pos):
                    self.selected_horse = 3
                
                # Start race
                elif self.buttons["RACE"].is_clicked(event.pos):
                    bet = self.bet_input.get_value()
                    if self.selected_horse is not None and 0 < bet <= self.player.money:
                        self.bet_amount = bet
                        self.player.bet(bet)
                        self.state = "RACING"
                        self.race_time = 0
            
            elif self.state == "RESULT":
                if self.buttons["PLAY_AGAIN"].is_clicked(event.pos):
                    self.reset_game()
        
        if self.state == "BETTING":
            self.bet_input.handle_event(event)
    
    def check_winner(self):
        """Determine the race winner."""
        # Find first horse to finish
        for i, horse in enumerate(self.horses):
            if horse.finished:
                self.winning_horse = i
                break
        
        if self.selected_horse == self.winning_horse:
            # Player won!
            payout = self.bet_amount * 3  # 3:1 payout for picking correct horse
            self.player.win(payout + self.bet_amount, "horse_racing")
            self.result_message = f"🎉 {self.horses[self.winning_horse].name} wins! You picked correctly! Win ${payout}!"
        else:
            self.result_message = f"{self.horses[self.winning_horse].name} wins the race! You picked {self.horses[self.selected_horse].name}. You lose."
    
    def update(self):
        if self.state == "RACING":
            # Update all horses
            all_finished = True
            for horse in self.horses:
                horse.update(True)
                if not horse.finished:
                    all_finished = False
            
            self.race_time += 1
            
            # Check if race is over
            if all_finished:
                self.check_winner()
                self.state = "RESULT"
    
    def draw(self, surface, current_money):
        # Draw title
        title = self.font_large.render("HORSE RACING", True, GOLD)
        surface.blit(title, (self.width // 2 - 180, 20))
        
        # Draw money
        money_text = self.font_small.render(f"Balance: ${current_money:,.2f}", True, WHITE)
        surface.blit(money_text, (20, 60))
        
        # Draw back button
        self.buttons["BACK"].draw(surface)
        
        # Draw race track
        self.draw_track(surface)
        
        # Draw all horses
        for horse in self.horses:
            horse.draw(surface, self.font_small)
        
        if self.state == "BETTING":
            # Draw betting options
            self.buttons["HORSE_1"].draw(surface)
            self.buttons["HORSE_2"].draw(surface)
            self.buttons["HORSE_3"].draw(surface)
            self.buttons["HORSE_4"].draw(surface)
            
            # Draw selected horse highlight
            if self.selected_horse is not None:
                selected_text = self.font_medium.render(f"Selected: {self.horses[self.selected_horse].name}", True, GOLD)
                surface.blit(selected_text, (self.width // 2 - 150, 430))
            
            # Draw bet amount input
            bet_label = self.font_medium.render("Bet Amount:", True, WHITE)
            surface.blit(bet_label, (self.width // 2 - 100, 450))
            self.bet_input.draw(surface)
            
            # Get bet amount from input
            if self.bet_input.get_value() > 0:
                self.bet_amount = self.bet_input.get_value()
            
            self.buttons["RACE"].draw(surface)
        
        elif self.state == "RACING":
            race_text = self.font_medium.render("🏇 RACING... 🏇", True, GOLD)
            surface.blit(race_text, (self.width // 2 - 150, 430))
        
        elif self.state == "RESULT":
            # Draw result
            result_text = self.font_large.render(self.result_message, True, GOLD)
            surface.blit(result_text, (self.width // 2 - 350, 420))
            
            self.buttons["PLAY_AGAIN"].draw(surface)
    
    def draw_track(self, surface):
        """Draw the race track."""
        # Draw finish line
        finish_x = self.track_end_x
        pygame.draw.line(surface, GOLD, (finish_x, 120), (finish_x, 400), 3)
        pygame.draw.line(surface, GOLD, (finish_x + 2, 120), (finish_x + 2, 400), 3)
        
        # Draw track background lines
        for horse in self.horses:
            pygame.draw.line(surface, GRAY, (self.track_start_x, horse.y + 10), (self.track_end_x, horse.y + 10), 1)
    
    def reset_game(self):
        """Reset for next game."""
        self.state = "BETTING"
        self.selected_horse = None
        self.bet_amount = 0
        self.result_message = ""
        self.winning_horse = None
        self.race_time = 0
        self.bet_input.text = ""
        
        # Reset all horses
        for horse in self.horses:
            horse.reset()
