import random


class AI:
    def __init__(self, player_color):
        self.player_color = player_color

    def find_random_valid_move(self, valid_moves):
        """Find and return a random valid move."""
        if valid_moves:
            return random.choice(valid_moves)
        return None
