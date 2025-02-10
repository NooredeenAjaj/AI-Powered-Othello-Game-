from ui.ui import UI
import pygame
from ai.ai import AI
from board.board import Board
from ai.aiadv import AI_adv


def main():

    ui = UI()

    board = Board()
    aiadvans = AI_adv("W")
    running = True
    current_player = "B"
    for p in board.get_all_valid_moves("B"):

        print(p.row, p.col)
    while running:
        if current_player == "B":
            valid_moves = board.get_all_valid_moves(current_player)
            if not valid_moves:
                print("No valid moves for Human, AI will play...")
                current_player = "W"
                continue

            move = ui.update(board.board)
            if move:

                board.make_move(move, current_player)
                board.flip_pieces(move, current_player)
                current_player = board.get_opponent(current_player)
                print("your teurn is done")

        else:

            print("ai will play")
            move = aiadvans.adversarial_search(board)
            print("ai is done")
            if move:
                board.make_move(move, current_player)
                board.flip_pieces(move, current_player)
                current_player = board.get_opponent(current_player)
                print(board.score())
                # pygame.time.delay(2000)
            else:
                valid_moves = board.get_all_valid_moves(current_player)
                print("ai passes the game ")
                print(len(valid_moves))
                current_player = board.get_opponent(current_player)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()


if __name__ == "__main__":
    main()
