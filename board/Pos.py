class Pos:
    """Class to handle positions on the board."""

    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __add__(self, direction):
        """Add a direction to a position."""
        return Pos(self.row + direction.delta_row, self.col + direction.delta_col)
