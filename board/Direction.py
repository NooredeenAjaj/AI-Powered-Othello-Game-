class Direction:
    """Class to define directions for movement on the board."""

    def __init__(self, delta_row, delta_col):
        self.delta_row = delta_row
        self.delta_col = delta_col
