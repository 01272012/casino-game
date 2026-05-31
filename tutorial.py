import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
RED = (220, 20, 60)
GREEN = (0, 128, 0)
BLUE = (70, 130, 180)
LIGHT_GRAY = (200, 200, 200)

class Tutorial:
    """Tutorial system for walking through each game."""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        self.font_tiny = pygame.font.Font(None, 18)
        
        # Tutorial data for each game
        self.tutorials = {
            "BLACKJACK": [
                {
                    "title": "BLACKJACK - How to Play",
                    "steps": [
                        "1. Goal: Get cards totaling 21 or beat the dealer without going over",
                        "2. Place your bet amount and click 'Place Bet'",
                        "3. You'll be dealt 2 cards, dealer gets 2 (one hidden)",
                        "4. Choose your action:",
                        "   • HIT - Take another card",
                        "   • STAND - Keep your hand and let dealer play",
                        "   • DOUBLE - Double bet and take 1 card (risky!)",
                        "5. If you reach 21 - BLACKJACK! You win 1.5x your bet",
                        "6. If dealer busts (goes over 21) - You win!",
                        "7. If you have higher total than dealer - You win 2x your bet"
                    ]
                }
            ],
            "SLOTS": [
                {
                    "title": "SLOTS - How to Play",
                    "steps": [
                        "1. Goal: Spin the reels and match symbols",
                        "2. Enter your bet amount and click 'Spin for $'",
                        "3. The 3 reels will spin with random symbols",
                        "4. Symbols include: 🍒 🍊 🍋 🍇 🔔 💎",
                        "5. Results:",
                        "   • 3 matching symbols = JACKPOT! 10x your bet",
                        "   • 2 matching symbols = WIN! 2x your bet",
                        "   • No match = You lose",
                        "6. Click 'Play Again' to spin again",
                        "7. No skill involved - pure luck!"
                    ]
                }
            ],
            "ROULETTE": [
                {
                    "title": "ROULETTE - How to Play",
                    "steps": [
                        "1. Goal: Predict where the ball will land on the wheel",
                        "2. Choose a bet type by clicking a button:",
                        "   • RED or BLACK = 2:1 payout",
                        "   • GREEN (0) = 36:1 payout",
                        "   • Specific number (0-36) = 36:1 payout",
                        "3. Enter your bet amount",
                        "4. Click SPIN! to spin the wheel",
                        "5. Watch the wheel rotate and slow down",
                        "6. The pointer at top shows the winning number",
                        "7. If you picked correctly - You win!",
                        "8. Red numbers: 1-7, 12-18, 19-25, 30-36"
                    ]
                }
            ],
            "HORSE_RACING": [
                {
                    "title": "HORSE RACING - How to Play",
                    "steps": [
                        "1. Goal: Pick the winning horse",
                        "2. 4 horses compete: Thunder, Lightning, Storm, Blaze",
                        "3. Each horse has different speed and stamina",
                        "4. Click on a horse button to select it",
                        "5. Enter your bet amount",
                        "6. Click START RACE! to begin",
                        "7. Watch each horse race across the track",
                        "8. Stamina bars show above each horse",
                        "9. Horses slow down as stamina decreases",
                        "10. First horse to finish line wins! 3x payout if you picked right"
                    ]
                }
            ],
            "POOL": [
                {
                    "title": "POOL - How to Play",
                    "steps": [
                        "1. Goal: Pot (sink) as many balls as possible",
                        "2. Enter your bet amount and click 'Play'",
                        "3. You'll see a pool table with cue ball and 15 numbered balls",
                        "4. Aiming Phase:",
                        "   • Move mouse to aim (golden line shows direction)",
                        "   • Press UP/DOWN arrow keys to set power (0-100)",
                        "   • Watch the power bar fill up",
                        "5. Click SHOOT to take your shot",
                        "6. Physics Engine:",
                        "   • Balls collide realistically",
                        "   • Balls bounce off walls",
                        "   • Balls slow down due to friction",
                        "7. Earn money for each ball potted:",
                        "   • 1 ball = 2x bet | 2 balls = 3x bet | 3+ = profit scales!"
                    ]
                }
            ]
        }
    
    def draw_tutorial(self, surface, game_name):
        """Draw tutorial screen for a specific game."""
        if game_name not in self.tutorials:
            return
        
        tutorial = self.tutorials[game_name][0]
        
        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(240)
        overlay.fill(BLACK)
        surface.blit(overlay, (0, 0))
        
        # Tutorial box
        box_width = 900
        box_height = 600
        box_x = (self.width - box_width) // 2
        box_y = (self.height - box_height) // 2
        
        pygame.draw.rect(surface, BLUE, (box_x, box_y, box_width, box_height))
        pygame.draw.rect(surface, GOLD, (box_x, box_y, box_width, box_height), 3)
        
        # Title
        title_text = self.font_large.render(tutorial["title"], True, GOLD)
        surface.blit(title_text, (box_x + 30, box_y + 20))
        
        # Steps
        y_offset = box_y + 80
        line_height = 28
        
        for i, step in enumerate(tutorial["steps"]):
            step_text = self.font_small.render(step, True, WHITE)
            surface.blit(step_text, (box_x + 40, y_offset + i * line_height))
        
        # Instructions at bottom
        inst_text = self.font_tiny.render("Press SPACE to continue or ESC to skip", True, LIGHT_GRAY)
        surface.blit(inst_text, (box_x + 30, box_y + box_height - 35))

class TutorialManager:
    """Manages tutorial state across games."""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tutorial = Tutorial(width, height)
        self.active_tutorial = None  # Which game's tutorial is showing
        self.tutorials_completed = set()
    
    def show_tutorial(self, game_name):
        """Start showing tutorial for a game."""
        if game_name not in self.tutorials_completed:
            self.active_tutorial = game_name
            return True
        return False
    
    def skip_tutorial(self):
        """Skip current tutorial."""
        if self.active_tutorial:
            self.tutorials_completed.add(self.active_tutorial)
            self.active_tutorial = None
    
    def complete_tutorial(self):
        """Mark tutorial as completed and move to game."""
        if self.active_tutorial:
            self.tutorials_completed.add(self.active_tutorial)
            game = self.active_tutorial
            self.active_tutorial = None
            return game
        return None
    
    def handle_event(self, event):
        """Handle events while tutorial is showing."""
        if self.active_tutorial and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                return self.complete_tutorial()
            elif event.key == pygame.K_ESCAPE:
                self.skip_tutorial()
                return self.active_tutorial  # Still start the game
        return None
    
    def draw(self, surface):
        """Draw active tutorial."""
        if self.active_tutorial:
            self.tutorial.draw_tutorial(surface, self.active_tutorial)
