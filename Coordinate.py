class Coordinate:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def get_tuple(self):
        return self.row, self.col

    def move(self, vector):
        row, col = vector
        self.row += row
        self.col += col
