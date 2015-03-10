# Data for the threes game

def _blanks(rows=4, columns=4):
    return [[None] * columns] * rows

class Tile(object):

    def __init__(self, board, position, value=None):
        self.value = value  # Integer in {1, 2, 3 * 2 ** n for n = 0, 1, ...}
        self.board = board  # The board to which this tile belongs
        self.position = position  # (row, column) of this tile in board
        self.row, self.column = self.position
        # Maybe add some validation here ...

    @property
    def left_neighbor(self):
        if self.row <= 0:
            return None
        else:
            return self.board[self.row - 1][self.column]

    @property
    def right_neighbor(self):
        if self.row >= (self.board.rows - 1):
            return None
        else:
            return self.board[self.row + 1][self.column]

    @property
    def upper_neighbor(self):
        if self.column <= 0:
            return None
        else:
            return self.board[self.row ][self.column - 1]

    @property
    def lower_neighbor(self):
        if self.column >= (self.board.columns - 1):
            return None
        else:
            return self.board[self.row][self.column + 1]

    @property
    def neighbors(self):
        return [self.left_neighbor,
                self.right_neighbor,
                self.upper_neighbor,
                self.lower_neighbor]


class Board(list):  # we want indexing/slicing, along with some helper functions
    """A nested list of tiles for the Threes game"""
    def __init__(self, data=None, rows=4, columns=4):
        """Build a board from data. If data is provided, rows and columns are ignored
        If no data is provided, we build an empty board if rows by columns"""
        list.__init__(self)
        if data is None:
            data = _blanks(rows, columns)
            self.rows = rows
            self.columns = columns
        else:
            self.rows = len(data)
            self.columns = len(data[0])

        for row in xrange(rows):
            self.append([])
            for col in xrange(columns):
                self[row].append(Tile(self, (row, col), data[row][col]))

    @property
    def values(self):
        return [
            [tile.value for tile in row] for row in self
        ]
