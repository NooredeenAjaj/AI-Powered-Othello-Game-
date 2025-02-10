import unittest

from board.Pos import Pos
from board.Direction import Direction
from board.board import Board


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_initial_setup(self):
        """Testar att brädan initieras korrekt med de fyra startbrickorna."""
        self.assertEqual(self.board.board[3][3], "W")
        self.assertEqual(self.board.board[3][4], "B")
        self.assertEqual(self.board.board[4][3], "B")
        self.assertEqual(self.board.board[4][4], "W")

    def test_get_opponent(self):
        """Testar att `get_opponent` returnerar rätt motståndare."""
        self.assertEqual(self.board.get_opponent("W"), "B")
        self.assertEqual(self.board.get_opponent("B"), "W")

    def test_make_move(self):
        """Testar att `make_move` placerar en pjäs korrekt."""
        self.board.make_move(Pos(2, 3), "W")
        self.assertEqual(self.board.board[2][3], "W")

    def test_flip_pieces(self):
        """Testar att `flip_pieces` vänder motståndarens pjäser korrekt."""
        self.board.make_move(Pos(2, 3), "B")
        self.board.flip_pieces(Pos(2, 3), "B")
        self.assertEqual(self.board.board[3][3], "B")

    def test_get_all_valid_moves(self):
        """Testar att `get_all_valid_moves` returnerar korrekta drag för en spelare."""

        valid_moves = self.board.get_all_valid_moves("B")
        print(valid_moves[0])
        self.assertIn(Pos(3, 2), valid_moves)
        self.assertIn(Pos(2, 3), valid_moves)
        self.assertIn(Pos(4, 5), valid_moves)
        self.assertIn(Pos(5, 4), valid_moves)

    def test_is_within_bounds(self):
        """Testar att `is_within_bounds` fungerar korrekt."""
        self.assertTrue(self.board.is_within_bounds(Pos(0, 0)))
        self.assertTrue(self.board.is_within_bounds(Pos(7, 7)))
        self.assertFalse(self.board.is_within_bounds(Pos(-1, 0)))
        self.assertFalse(self.board.is_within_bounds(Pos(8, 8)))

    def test_score(self):
        score = self.board.score()
        self.assertEqual(score["B"], 2)
        self.assertEqual(score["W"], 2)

    def test_is_full(self):
        """Testar att `is_full` returnerar False på en tom bräda och True på en full."""
        self.assertFalse(self.board.is_full())

        # Fyll hela brädan
        for r in range(8):
            for c in range(8):
                self.board.board[r][c] = "B"

        self.assertTrue(self.board.is_full())


if __name__ == "__main__":
    unittest.main()
