class Player:
    def __init__(self, start_money=1000):
        self.money = start_money
        self.total_wins = 0
        self.total_bets = 0
        self.games_played = {
            "blackjack": 0,
            "slots": 0,
            "roulette": 0,
            "pool": 0,
            "horse_racing": 0
        }
        self.games_won = {
            "blackjack": 0,
            "slots": 0,
            "roulette": 0,
            "pool": 0,
            "horse_racing": 0
        }
    
    def bet(self, amount):
        """Place a bet. Returns True if successful."""
        if amount <= self.money:
            self.money -= amount
            self.total_bets += amount
            return True
        return False
    
    def win(self, amount, game_name):
        """Win money and update stats."""
        self.money += amount
        self.total_wins += amount
        self.games_won[game_name] += 1
    
    def lose(self, game_name):
        """Update loss stats."""
        pass
    
    def play_game(self, game_name):
        """Record that a game was played."""
        self.games_played[game_name] += 1
    
    def get_win_rate(self):
        """Calculate overall win rate."""
        total_games = sum(self.games_played.values())
        if total_games == 0:
            return 0
        total_wins_count = sum(self.games_won.values())
        return (total_wins_count / total_games) * 100
