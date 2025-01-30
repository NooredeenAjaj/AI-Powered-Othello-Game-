from ui.ui import UI
import pygame
from ai.ai import AI


class Direction:
    """Class to define directions for movement on the board."""

    def __init__(self, delta_row, delta_col):
        self.delta_row = delta_row
        self.delta_col = delta_col


class Pos:
    """Class to handle positions on the board."""

    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __add__(self, direction):
        """Add a direction to a position."""
        return Pos(self.row + direction.delta_row, self.col + direction.delta_col)


# Define all eight possible directions in Othello
DIRECTIONS = [
    Direction(-1, 0),  # Up
    Direction(1, 0),  # Down
    Direction(0, -1),  # Left
    Direction(0, 1),  # Right
    Direction(-1, -1),  # Up-Left
    Direction(-1, 1),  # Up-Right
    Direction(1, -1),  # Down-Left
    Direction(1, 1),  # Down-Right
]


def main():
    board = [
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, "W", "B", None, None, None],
        [None, None, None, "B", "W", None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
    ]

    ui = UI()

    ai = AI("W")  # Assuming AI is white
    running = True
    current_player = "B"  # Human starts as black

    while running:
        if current_player == "B":
            move = ui.update(board)  # Human move
            if move and is_valid_move(board, *move, current_player):
                make_move(board, *move, current_player)
                current_player = "W"
            elif move:
                print("Invalid move!")
        else:
            move = ai.make_move(board, is_valid_move, make_move)  # AI move
            if move:
                current_player = "B"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()


# Edge Case Handling: The function breaks the loop as soon as one valid direction is found.
# This is appropriate for determining if a move is valid but remember to handle the capturing
# or all valid directions when the move is made.
def is_valid_move(board, row, col, player):
    if board[row][col] is not None:
        return False  # Cannot place a piece on an already occupied square

    opponent = "W" if player == "B" else "B"
    valid = False

    for direction in DIRECTIONS:
        pos = Pos(row, col) + direction
        if is_within_bounds(pos, len(board)) and board[pos.row][pos.col] == opponent:
            # Move in the direction while the next cell contains the opponent's piece
            pos += direction
            while (
                is_within_bounds(pos, len(board))
                and board[pos.row][pos.col] == opponent
            ):
                pos += direction
            # Check if the line ends with the player's piece
            if is_within_bounds(pos, len(board)) and board[pos.row][pos.col] == player:
                valid = True
                break

    return valid


def is_within_bounds(pos, size):
    return 0 <= pos.row < size and 0 <= pos.col < size


def make_move(board, row, col, player):
    board[row][col] = player  # Place the player's disc


if __name__ == "__main__":
    main()
