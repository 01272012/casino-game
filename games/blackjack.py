import pygame
import random
from ui import Button, TextInput

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
RED = (220, 20, 60)
GREEN = (0, 128, 0)
BLUE = (70, 130, 180)

class Card:
    suits = ['♠', '♥', '♦', '♣']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
    
    def get_value(self):
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11
        else:
            return int(self.rank)
    
    def __str__(self):
        return f"{self.rank}{self.suit}"

class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for rank in Card.ranks for suit in Card.suits]
        random.shuffle(self.cards)
    
    def draw(self):
        if len(self.cards) < 10:
            self.__init__()  # Reshuffle if deck is low
        return self.cards.pop()

class BlackjackGame:
    def __init__(self, player, width, height):
        self.player = player
        self.width = width
        self.height = height
        
        self.deck = Deck()
        self.player_hand = []
        self.dealer_hand = []
        self.player_money = player.money
        
        self.state = "BETTING"  # BETTING, PLAYING, DEALER_TURN, RESULT
        self.bet_amount = 0
        self.message = "Place your bet"
        self.result = ""
        
        # UI
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        self.bet_input = TextInput(self.width // 2 - 100, 300, 200)
        self.buttons = {
            "HIT": Button(200, 500, 120, 50, "Hit", 24),
            "STAND": Button(350, 500, 120, 50, "Stand", 24),
            "DOUBLE": Button(500, 500, 120, 50, "Double", 24),
            "PLACE_BET": Button(self.width // 2 - 75, 380, 150, 50, "Place Bet", 24),
            "PLAY_AGAIN": Button(self.width // 2 - 75, 500, 150, 50, "Play Again", 24),
            "BACK": Button(20, 20, 100, 40, "Back", 20),
        }
        self.player.play_game("blackjack")
    
    def calculate_hand_value(self, hand):
        total = 0
        aces = 0
        
        for card in hand:
            total += card.get_value()
            if card.rank == 'A':
                aces += 1
        
        # Adjust for aces
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
        
        return total
    
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
                        self.start_game()
                        self.state = "PLAYING"
            
            elif self.state == "PLAYING":
                if self.buttons["HIT"].is_clicked(event.pos):
                    self.player_hand.append(self.deck.draw())
                    if self.calculate_hand_value(self.player_hand) > 21:
                        self.state = "RESULT"
                        self.result = "BUST! You lose."
                
                elif self.buttons["STAND"].is_clicked(event.pos):
                    self.state = "DEALER_TURN"
                
                elif self.buttons["DOUBLE"].is_clicked(event.pos):
                    if self.player.money >= self.bet_amount:
                        self.player.bet(self.bet_amount)
                        self.bet_amount *= 2
                        self.player_hand.append(self.deck.draw())
                        if self.calculate_hand_value(self.player_hand) > 21:
                            self.state = "RESULT"
                            self.result = "BUST! You lose."
                        else:
                            self.state = "DEALER_TURN"
            
            elif self.state == "RESULT":
                if self.buttons["PLAY_AGAIN"].is_clicked(event.pos):
                    self.reset_game()
        
        if self.state == "BETTING":
            self.bet_input.handle_event(event)
    
    def start_game(self):
        self.player_hand = [self.deck.draw(), self.deck.draw()]
        self.dealer_hand = [self.deck.draw(), self.deck.draw()]
    
    def dealer_play(self):
        """Dealer plays (must hit until 17+)"""
        while self.calculate_hand_value(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deck.draw())
    
    def determine_winner(self):
        player_value = self.calculate_hand_value(self.player_hand)
        dealer_value = self.calculate_hand_value(self.dealer_hand)
        
        if dealer_value > 21:
            winnings = self.bet_amount * 2
            self.player.win(winnings, "blackjack")
            self.result = f"Dealer busts! You win ${winnings}!"
        elif player_value > dealer_value:
            winnings = self.bet_amount * 2
            self.player.win(winnings, "blackjack")
            self.result = f"You win ${winnings}!"
        elif player_value == dealer_value:
            self.player.money += self.bet_amount  # Push
            self.result = "Push! Bet returned."
        else:
            self.result = f"Dealer wins. You lose ${self.bet_amount}."
    
    def update(self):
        if self.state == "DEALER_TURN":
            self.dealer_play()
            self.determine_winner()
            self.state = "RESULT"
    
    def draw(self, surface, current_money):
        # Draw title
        title = self.font_large.render("BLACKJACK", True, GOLD)
        surface.blit(title, (self.width // 2 - 150, 20))
        
        # Draw money
        money_text = self.font_small.render(f"Balance: ${current_money:,.2f}", True, WHITE)
        surface.blit(money_text, (20, 60))
        
        # Draw back button
        self.buttons["BACK"].draw(surface)
        
        if self.state == "BETTING":
            prompt = self.font_medium.render("Enter bet amount:", True, WHITE)
            surface.blit(prompt, (self.width // 2 - 150, 250))
            self.bet_input.draw(surface)
            self.buttons["PLACE_BET"].draw(surface)
        
        elif self.state in ["PLAYING", "DEALER_TURN"]:
            # Draw dealer cards
            dealer_label = self.font_medium.render("Dealer", True, WHITE)
            surface.blit(dealer_label, (50, 150))
            for i, card in enumerate(self.dealer_hand):
                self.draw_card(surface, card, 50 + i * 100, 200)
            dealer_value = self.calculate_hand_value(self.dealer_hand)
            if self.state == "PLAYING" and len(self.dealer_hand) == 2:
                # Hide second card while playing
                value_text = self.font_small.render(f"Value: {self.dealer_hand[0].get_value()}+?", True, WHITE)
            else:
                value_text = self.font_small.render(f"Value: {dealer_value}", True, WHITE)
            surface.blit(value_text, (50, 350))
            
            # Draw player cards
            player_label = self.font_medium.render("You", True, WHITE)
            surface.blit(player_label, (50, 400))
            for i, card in enumerate(self.player_hand):
                self.draw_card(surface, card, 50 + i * 100, 450)
            player_value = self.calculate_hand_value(self.player_hand)
            value_text = self.font_small.render(f"Value: {player_value}", True, WHITE)
            surface.blit(value_text, (50, 600))
            
            # Draw buttons
            if self.state == "PLAYING":
                self.buttons["HIT"].draw(surface)
                self.buttons["STAND"].draw(surface)
                self.buttons["DOUBLE"].draw(surface)
        
        elif self.state == "RESULT":
            result_text = self.font_large.render(self.result, True, GOLD)
            surface.blit(result_text, (self.width // 2 - 250, 250))
            
            # Show final hands
            dealer_value = self.calculate_hand_value(self.dealer_hand)
            player_value = self.calculate_hand_value(self.player_hand)
            
            dealer_label = self.font_medium.render(f"Dealer: {dealer_value}", True, WHITE)
            surface.blit(dealer_label, (50, 150))
            for i, card in enumerate(self.dealer_hand):
                self.draw_card(surface, card, 50 + i * 100, 200)
            
            player_label = self.font_medium.render(f"You: {player_value}", True, WHITE)
            surface.blit(player_label, (50, 400))
            for i, card in enumerate(self.player_hand):
                self.draw_card(surface, card, 50 + i * 100, 450)
            
            self.buttons["PLAY_AGAIN"].draw(surface)
    
    def draw_card(self, surface, card, x, y):
        card_width, card_height = 80, 120
        pygame.draw.rect(surface, WHITE, (x, y, card_width, card_height))
        pygame.draw.rect(surface, BLACK, (x, y, card_width, card_height), 2)
        
        # Determine color
        color = RED if card.suit in ['♥', '♦'] else BLACK
        
        rank_text = self.font_small.render(card.rank, True, color)
        suit_text = self.font_small.render(card.suit, True, color)
        
        surface.blit(rank_text, (x + 10, y + 10))
        surface.blit(suit_text, (x + 10, y + 50))
    
    def reset_game(self):
        self.player_hand = []
        self.dealer_hand = []
        self.state = "BETTING"
        self.bet_input.text = ""
        self.bet_amount = 0
        self.result = ""
        self.message = "Place your bet"
