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
            if move:

                make_move(board, *move, current_player)
                flip_pieces(board, *move, current_player, DIRECTIONS)

                current_player = "W"  # Switch to AI player after human move
        else:
            valid_moves = get_all_valid_moveis(board, current_player, DIRECTIONS)
            move = ai.find_random_valid_move(valid_moves)
            if move:

                make_move(board, move.row, move.col, current_player)
                flip_pieces(board, move.row, move.col, current_player, DIRECTIONS)

                current_player = "B"  # Switch back to human player after AI move

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()


# Edge Case Handling: The function breaks the loop as soon as one valid direction is found.
# This is appropriate for determining if a move is valid but remember to handle the capturing
# or all valid directions when the move is made.


def flip_pieces(board, row, col, player, DIRECTIONS):
    opponent = "W" if player == "B" else "B"
    size = len(board)
    to_flip = []

    # Kontrollera alla åtta möjliga riktningar
    for direction in DIRECTIONS:
        pieces = []
        next_pos = Pos(row + direction.delta_row, col + direction.delta_col)

        # Sök efter en kedja av motståndarens brickor
        while (
            is_within_bounds(next_pos, size)
            and board[next_pos.row][next_pos.col] == opponent
        ):
            pieces.append(next_pos)
            next_pos += direction

        # Kontrollera om kedjan avslutas med en av spelarens brickor
        if (
            is_within_bounds(next_pos, size)
            and board[next_pos.row][next_pos.col] == player
        ):
            to_flip.extend(pieces)

    # Vänd brickorna
    for pos in to_flip:
        board[pos.row][pos.col] = player

    return board


def get_all_valid_moveis(board, player, DIRECTIONS):
    positions = find_player_positions(board, player)
    valid_moves = []
    opponent = "W" if player == "B" else "B"
    size = len(board)  # Assuming a square board

    for pos in positions:
        for dir in DIRECTIONS:
            next_pos = pos + dir

            # Continue moving in direction until out of bounds or hits empty space
            while (
                is_within_bounds(next_pos, size)
                and board[next_pos.row][next_pos.col] is not None
            ):
                if board[next_pos.row][next_pos.col] == opponent:
                    next_pos += dir
                    if (
                        is_within_bounds(next_pos, size)
                        and board[next_pos.row][next_pos.col] == None
                    ):
                        if next_pos not in valid_moves:
                            valid_moves.append(next_pos)
                        break
                else:
                    break

    return valid_moves


def find_player_positions(board, player):
    positions = []
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == player:
                positions.append(Pos(row, col))
    return positions


def is_within_bounds(pos, size):
    return 0 <= pos.row < size and 0 <= pos.col < size


def make_move(board, row, col, player):
    board[row][col] = player  # Place the player's disc


if __name__ == "__main__":
    main()
