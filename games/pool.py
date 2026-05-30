import pygame
import math
from ui import Button, TextInput

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
RED = (220, 20, 60)
DARK_GREEN = (0, 100, 0)
LIGHT_GREEN = (144, 238, 144)
BLUE = (70, 130, 180)
GRAY = (128, 128, 128)

class Ball:
    """Represents a pool ball."""
    RADIUS = 8
    FRICTION = 0.98  # Friction coefficient
    POCKET_RADIUS = 15
    
    def __init__(self, x, y, ball_id=0, is_white=False):
        self.x = x
        self.y = y
        self.vx = 0  # Velocity X
        self.vy = 0  # Velocity Y
        self.ball_id = ball_id  # 0=white, 1-7=solid, 8=black, 9-15=striped
        self.is_white = is_white
        self.is_moving = False
        self.potted = False
        
        # Color based on ball type
        if is_white:
            self.color = WHITE
        elif ball_id == 0:
            self.color = WHITE
        elif ball_id == 8:
            self.color = BLACK
        elif ball_id <= 7:  # Solid balls (1-7)
            self.color = RED if ball_id % 2 == 1 else BLUE
        else:  # Striped balls (9-15)
            self.color = RED if (ball_id - 8) % 2 == 1 else BLUE
    
    def update(self, table_width, table_height, balls):
        """Update ball position and handle collisions."""
        if self.potted or (abs(self.vx) < 0.1 and abs(self.vy) < 0.1):
            self.is_moving = False
            self.vx = 0
            self.vy = 0
            return
        
        # Apply friction
        self.vx *= self.FRICTION
        self.vy *= self.FRICTION
        
        # Update position
        self.x += self.vx
        self.y += self.vy
        
        # Check table boundaries (bounce off walls)
        if self.x - self.RADIUS < 0:
            self.x = self.RADIUS
            self.vx *= -0.8
        elif self.x + self.RADIUS > table_width:
            self.x = table_width - self.RADIUS
            self.vx *= -0.8
        
        if self.y - self.RADIUS < 0:
            self.y = self.RADIUS
            self.vy *= -0.8
        elif self.y + self.RADIUS > table_height:
            self.y = table_height - self.RADIUS
            self.vy *= -0.8
        
        # Check collisions with other balls
        for other in balls:
            if other == self or other.potted:
                continue
            
            dx = other.x - self.x
            dy = other.y - self.y
            dist = math.sqrt(dx*dx + dy*dy)
            
            if dist < self.RADIUS * 2 and dist > 0:
                # Simple elastic collision
                angle = math.atan2(dy, dx)
                
                # Transfer velocity
                v1_mag = math.sqrt(self.vx**2 + self.vy**2)
                v2_mag = math.sqrt(other.vx**2 + other.vy**2)
                
                # Exchange velocities along collision line
                self.vx = v2_mag * math.cos(angle) * 0.9
                self.vy = v2_mag * math.sin(angle) * 0.9
                
                other.vx = v1_mag * math.cos(angle + math.pi) * 0.9
                other.vy = v1_mag * math.sin(angle + math.pi) * 0.9
                
                # Separate balls to prevent sticking
                overlap = self.RADIUS * 2 - dist
                self.x -= overlap/2 * math.cos(angle)
                self.y -= overlap/2 * math.sin(angle)
                other.x += overlap/2 * math.cos(angle)
                other.y += overlap/2 * math.sin(angle)
    
    def check_potted(self, pockets):
        """Check if ball went into a pocket."""
        for pocket in pockets:
            dx = self.x - pocket[0]
            dy = self.y - pocket[1]
            dist = math.sqrt(dx*dx + dy*dy)
            if dist < self.POCKET_RADIUS:
                self.potted = True
                return True
        return False
    
    def draw(self, surface):
        """Draw the ball."""
        if not self.potted:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.RADIUS)
            pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.RADIUS, 1)
            
            # Draw stripe or number indicator
            if self.ball_id > 8:  # Striped
                pygame.draw.circle(surface, GRAY, (int(self.x), int(self.y)), self.RADIUS - 3, 1)

class PoolGame:
    def __init__(self, player, width, height):
        self.player = player
        self.width = width
        self.height = height
        
        self.state = "BETTING"  # BETTING, AIMING, SHOOTING, PLAYING, RESULT
        self.bet_amount = 0
        self.balls_potted = 0
        self.result_message = ""
        
        # Fonts
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 28)
        self.font_small = pygame.font.Font(None, 20)
        
        # Table dimensions
        self.table_x = 150
        self.table_y = 80
        self.table_width = 700
        self.table_height = 400
        
        # Pockets (corners and sides)
        self.pockets = [
            (self.table_x, self.table_y),  # Top-left
            (self.table_x + self.table_width // 2, self.table_y),  # Top-middle
            (self.table_x + self.table_width, self.table_y),  # Top-right
            (self.table_x, self.table_y + self.table_height),  # Bottom-left
            (self.table_x + self.table_width // 2, self.table_y + self.table_height),  # Bottom-middle
            (self.table_x + self.table_width, self.table_y + self.table_height),  # Bottom-right
        ]
        
        # Initialize balls
        self.cue_ball = Ball(self.table_x + 150, self.table_y + self.table_height // 2, is_white=True)
        self.balls = [self.cue_ball]
        
        # Create pool balls (1-15)
        rack_x = self.table_x + self.table_width - 200
        rack_y = self.table_y + self.table_height // 2
        spacing = Ball.RADIUS * 2.2
        
        ball_id = 1
        for row in range(5):
            for col in range(row + 1):
                x = rack_x + row * spacing
                y = rack_y - (row * spacing / 2) + col * spacing
                self.balls.append(Ball(x, y, ball_id))
                ball_id += 1
        
        # Aiming system
        self.aim_angle = 0  # Angle in radians
        self.aim_power = 0  # Power 0-100
        self.mouse_pos = (0, 0)
        
        # UI
        self.bet_input = TextInput(self.width // 2 - 75, 520, 150)
        
        self.buttons = {
            "PLACE_BET": Button(self.width // 2 - 75, 570, 150, 50, "Play", 24),
            "SHOOT": Button(50, 550, 100, 50, "SHOOT", 28),
            "RESET": Button(170, 550, 100, 50, "Reset", 28),
            "PLAY_AGAIN": Button(self.width // 2 - 75, 550, 150, 50, "Play Again", 24),
            "BACK": Button(20, 20, 100, 40, "Back", 20),
        }
        
        self.player.play_game("pool")
    
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
                        self.state = "AIMING"
            
            elif self.state == "AIMING":
                if self.buttons["SHOOT"].is_clicked(event.pos):
                    # Calculate velocity based on angle and power
                    vx = math.cos(self.aim_angle) * self.aim_power / 10
                    vy = math.sin(self.aim_angle) * self.aim_power / 10
                    self.cue_ball.vx = vx
                    self.cue_ball.vy = vy
                    self.state = "SHOOTING"
                    self.aim_power = 0
                
                elif self.buttons["RESET"].is_clicked(event.pos):
                    self.reset_game()
            
            elif self.state == "RESULT":
                if self.buttons["PLAY_AGAIN"].is_clicked(event.pos):
                    self.reset_game()
        
        elif event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos
            
            if self.state == "AIMING":
                # Calculate aiming angle from cue ball to mouse
                dx = self.mouse_pos[0] - self.cue_ball.x
                dy = self.mouse_pos[1] - self.cue_ball.y
                self.aim_angle = math.atan2(dy, dx)
        
        elif event.type == pygame.KEYDOWN:
            if self.state == "AIMING":
                if event.key == pygame.K_UP:
                    self.aim_power = min(100, self.aim_power + 5)
                elif event.key == pygame.K_DOWN:
                    self.aim_power = max(0, self.aim_power - 5)
        
        if self.state == "BETTING":
            self.bet_input.handle_event(event)
    
    def update(self):
        if self.state == "SHOOTING":
            # Update all balls
            for ball in self.balls:
                ball.update(self.table_x + self.table_width, self.table_y + self.table_height, self.balls)
            
            # Check for potted balls
            for ball in self.balls:
                if not ball.potted and ball.check_potted(self.pockets):
                    if not ball.is_white:
                        self.balls_potted += 1
            
            # Check if all balls have stopped
            all_stopped = True
            for ball in self.balls:
                if abs(ball.vx) > 0.1 or abs(ball.vy) > 0.1:
                    all_stopped = False
                    break
            
            if all_stopped:
                self.state = "PLAYING"
                self.finish_round()
    
    def finish_round(self):
        """End the round and calculate results."""
        if self.balls_potted > 0:
            payout = self.bet_amount * (1 + self.balls_potted)
            self.player.win(payout + self.bet_amount, "pool")
            self.result_message = f"You potted {self.balls_potted} ball(s)! You win ${payout}!"
        else:
            self.result_message = "No balls potted. You lose."
        
        self.state = "RESULT"
    
    def draw(self, surface, current_money):
        # Draw title
        title = self.font_large.render("POOL", True, GOLD)
        surface.blit(title, (self.width // 2 - 80, 20))
        
        # Draw money
        money_text = self.font_small.render(f"Balance: ${current_money:,.2f}", True, WHITE)
        surface.blit(money_text, (20, 50))
        
        # Draw back button
        self.buttons["BACK"].draw(surface)
        
        if self.state == "BETTING":
            # Draw betting UI
            bet_label = self.font_medium.render("Bet Amount:", True, WHITE)
            surface.blit(bet_label, (self.width // 2 - 100, 490))
            self.bet_input.draw(surface)
            self.buttons["PLACE_BET"].draw(surface)
        
        else:
            # Draw pool table
            self.draw_pool_table(surface)
            
            # Draw all balls
            for ball in self.balls:
                ball.draw(surface)
            
            # Draw pockets
            for pocket in self.pockets:
                pygame.draw.circle(surface, BLACK, pocket, Ball.POCKET_RADIUS, 2)
            
            if self.state == "AIMING":
                # Draw aiming line
                length = 100
                aim_end_x = self.cue_ball.x + math.cos(self.aim_angle) * length
                aim_end_y = self.cue_ball.y + math.sin(self.aim_angle) * length
                pygame.draw.line(surface, GOLD, (self.cue_ball.x, self.cue_ball.y), (aim_end_x, aim_end_y), 2)
                
                # Draw power indicator
                power_text = self.font_small.render(f"Power: {int(self.aim_power)}", True, WHITE)
                surface.blit(power_text, (50, 500))
                pygame.draw.rect(surface, GRAY, (50, 525, 200, 20))
                pygame.draw.rect(surface, GOLD, (50, 525, int(self.aim_power * 2), 20))
                
                # Draw instructions
                inst_text = self.font_small.render("UP/DOWN = Power | Click SHOOT", True, WHITE)
                surface.blit(inst_text, (50, 560))
                
                self.buttons["SHOOT"].draw(surface)
                self.buttons["RESET"].draw(surface)
            
            elif self.state in ["SHOOTING", "PLAYING"]:
                status_text = self.font_medium.render("Balls in motion...", True, GOLD)
                surface.blit(status_text, (self.width // 2 - 150, 500))
            
            elif self.state == "RESULT":
                result_text = self.font_large.render(self.result_message, True, GOLD)
                surface.blit(result_text, (self.width // 2 - 300, 500))
                self.buttons["PLAY_AGAIN"].draw(surface)
    
    def draw_pool_table(self, surface):
        """Draw the pool table."""
        # Table background
        pygame.draw.rect(surface, DARK_GREEN, (self.table_x, self.table_y, self.table_width, self.table_height))
        
        # Table border
        pygame.draw.rect(surface, GOLD, (self.table_x, self.table_y, self.table_width, self.table_height), 3)
        
        # Center spot
        center_x = self.table_x + self.table_width // 2
        center_y = self.table_y + self.table_height // 2
        pygame.draw.circle(surface, LIGHT_GREEN, (center_x, center_y), 3)
    
    def reset_game(self):
        """Reset for next game."""
        self.state = "AIMING"
        self.bet_input.text = ""
        self.balls_potted = 0
        self.result_message = ""
        
        # Reset cue ball
        self.cue_ball.x = self.table_x + 150
        self.cue_ball.y = self.table_y + self.table_height // 2
        self.cue_ball.vx = 0
        self.cue_ball.vy = 0
        self.cue_ball.potted = False
        
        # Reset other balls
        rack_x = self.table_x + self.table_width - 200
        rack_y = self.table_y + self.table_height // 2
        spacing = Ball.RADIUS * 2.2
        
        ball_id = 1
        for i in range(1, len(self.balls)):
            row = 0
            count = 0
            for r in range(5):
                if ball_id - 1 < r * (r + 1) // 2 + r:
                    row = r
                    break
            
            col = (ball_id - 1) - (row * (row + 1) // 2)
            
            self.balls[i].x = rack_x + row * spacing
            self.balls[i].y = rack_y - (row * spacing / 2) + col * spacing
            self.balls[i].vx = 0
            self.balls[i].vy = 0
            self.balls[i].potted = False
            ball_id += 1
        
        self.aim_power = 0
