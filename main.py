from ui.ui import UI
import pygame
from ai.ai import AI
from board.board import Board
from ai.aiadv import AI_adv
from newwork.OthelloClient import OthelloClient


def main():

    ui = UI()
    ai = AI("W")
    board = Board()
    aiadvans = AI_adv("W")
    running = True
    current_player = "B"
    while running:
        if current_player == "B":
            move = ui.update(
                board.board
            )  # Assumed modification to UI's update to handle the board as 2D list
            if move:

                board.make_move(move, current_player)
                board.flip_pieces(move, current_player)
                current_player = "W"

        else:
            valid_moves = board.get_all_valid_moves(current_player)
            # move = ai.find_random_valid_move(valid_moves)
            # move = ai.find_best_move(board=board)
            move = aiadvans.adversarial_search(board)
            if move:
                board.make_move(move, current_player)
                board.flip_pieces(move, current_player)
                current_player = "B"
                print(board.score())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()


if __name__ == "__main__":
    main()
