import pygame
import sys


class UI:
    def __init__(self, board_size=8, cell_size=60):
        """Initialize the Pygame window and set up the board dimensions."""
        pygame.init()
        self.board_size = board_size
        self.cell_size = cell_size
        self.width = self.height = self.cell_size * board_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Othello Game")

        # Colors
        self.bg_color = pygame.Color("darkgreen")
        self.black = pygame.Color("black")
        self.white = pygame.Color("white")

    def draw_board(self, board):
        """Draw the board and the discs on it."""
        self.screen.fill(self.bg_color)
        for row in range(self.board_size):
            for col in range(self.board_size):
                x = col * self.cell_size
                y = row * self.cell_size
                pygame.draw.rect(
                    self.screen, self.black, (x, y, self.cell_size, self.cell_size), 1
                )
                if board[row][col] == "B":
                    pygame.draw.circle(
                        self.screen,
                        self.black,
                        (x + self.cell_size // 2, y + self.cell_size // 2),
                        self.cell_size // 3,
                    )
                elif board[row][col] == "W":
                    pygame.draw.circle(
                        self.screen,
                        self.white,
                        (x + self.cell_size // 2, y + self.cell_size // 2),
                        self.cell_size // 3,
                    )
        pygame.display.flip()

    def get_player_move(self, event):
        """Convert mouse clicks to board coordinates."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            col = x // self.cell_size
            row = y // self.cell_size
            return (row, col)
        return None

    def update(self, board):
        """Update the UI with the current state of the board."""
        self.draw_board(board)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return self.get_player_move(event)
        return None

    def display_winner(self, winner):
        """Display the game result."""
        font = pygame.font.Font(None, 72)
        text = font.render(f"{winner} Wins!", True, self.white, self.bg_color)
        text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()
