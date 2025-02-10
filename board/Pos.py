class Pos:
    """Class to handle positions on the board."""

    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __add__(self, direction):
        """Add a direction to a position."""
        return Pos(self.row + direction.delta_row, self.col + direction.delta_col)

    def __eq__(self, other):
        if isinstance(other, Pos):
            return self.row == other.row and self.col == other.col
        return False

    def __hash__(self):
        return hash((self.row, self.col))

    def __repr__(self):
        return f"Pos({self.row}, {self.col})"
