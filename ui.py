import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
LIGHT_GREEN = (144, 238, 144)
RED = (220, 20, 60)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER = (100, 150, 200)

class Button:
    def __init__(self, x, y, width, height, text, font_size=24):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.hovered = False
    
    def draw(self, surface):
        color = BUTTON_HOVER if self.hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, GOLD, self.rect, 3)
        
        text_surf = self.font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
    
    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Menu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font_large = pygame.font.Font(None, 72)
        self.font_small = pygame.font.Font(None, 24)
        
        # Create buttons
        button_width = 250
        button_height = 60
        button_x = (width - button_width) // 2
        
        self.buttons = {
            "BLACKJACK": Button(button_x, 150, button_width, button_height, "Blackjack", 28),
            "SLOTS": Button(button_x, 230, button_width, button_height, "Slots", 28),
            "ROULETTE": Button(button_x, 310, button_width, button_height, "Roulette", 28),
            "POOL": Button(button_x, 390, button_width, button_height, "Pool", 28),
            "HORSE_RACING": Button(button_x, 470, button_width, button_height, "Horse Racing", 28),
            "QUIT": Button(button_x, 550, button_width, button_height, "Quit", 28),
        }
        
        self.mouse_pos = (0, 0)
    
    def handle_click(self, pos):
        for key, button in self.buttons.items():
            if button.is_clicked(pos):
                return key
        return None
    
    def draw(self, surface, money, total_wins):
        # Title
        title = self.font_large.render("CASINO", True, GOLD)
        title_rect = title.get_rect(center=(self.width // 2, 50))
        surface.blit(title, title_rect)
        
        # Player stats
        stats_text = f"Balance: ${money:,.2f} | Total Wins: ${total_wins:,.2f}"
        stats = self.font_small.render(stats_text, True, WHITE)
        stats_rect = stats.get_rect(topleft=(20, 20))
        surface.blit(stats, stats_rect)
        
        # Draw buttons
        self.mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons.values():
            button.update(self.mouse_pos)
            button.draw(surface)

class TextInput:
    """Simple text input for betting amounts."""
    def __init__(self, x, y, width=200, height=40):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.font = pygame.font.Font(None, 32)
        self.active = True
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                return True  # Submit
            elif event.unicode.isdigit():
                self.text += event.unicode
        return False
    
    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)
        pygame.draw.rect(surface, GOLD, self.rect, 2)
        
        text_surf = self.font.render(self.text, True, BLACK)
        surface.blit(text_surf, (self.rect.x + 10, self.rect.y + 5))
    
    def get_value(self):
        try:
            return int(self.text) if self.text else 0
        except ValueError:
            return 0
