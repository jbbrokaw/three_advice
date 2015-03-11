# Data for the threes game
from __future__ import unicode_literals

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
        if self.column <= 0:
            return None
        else:
            return self.board[self.row][self.column - 1]

    @property
    def right_neighbor(self):
        if self.column >= (self.board.columns - 1):
            return None
        else:
            return self.board[self.row][self.column + 1]

    @property
    def upper_neighbor(self):
        if self.row <= 0:
            return None
        else:
            return self.board[self.row - 1][self.column]

    @property
    def lower_neighbor(self):
        if self.row >= (self.board.rows - 1):
            return None
        else:
            return self.board[self.row + 1][self.column]

    @property
    def neighbors(self):
        neighbor_list = list()
        if self.left_neighbor:
            neighbor_list.append(self.left_neighbor)
        if self.right_neighbor:
            neighbor_list.append(self.right_neighbor)
        if self.upper_neighbor:
            neighbor_list.append(self.upper_neighbor)
        if self.lower_neighbor:
            neighbor_list.append(self.lower_neighbor)

        return neighbor_list

    def shift(self, neighbor_attribute):
        """Move neighbor into self if possible, unless already shifted"""
        neighbor = self.__getattribute__(neighbor_attribute)
        if neighbor is None:
            return False  # Cannot have shifted at the last possibility

        if (  # We can combine here
                (self.value == neighbor.value) or
                ((self.value == 1) and (neighbor.value == 2)) or
                ((self.value == 2) and (neighbor.value == 1))
            ):
            self.value = self.value + neighbor.value
            neighbor.value = None
            neighbor.shift()
            # Don't care about return value of neighbor shift, we know we shifted
            return True
        elif self.value is None:  # Just move neighbor into this tile
            self.value = neighbor.value
            neighbor.value = None
            neighbor.shift()  # Don't care about return value, we know we shifted
            return True
        else:  # We cannot shift, try the next one in line
            return neighbor.shift(neighbor_attribute)


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

    def shift(self, direction):
        """Make a threes move, wherein you shift tiles up, down, left, or right"""
        if direction == "up":
            targets = self[0]
            neighbor_attribute = 'lower_neighbor'

        elif direction == "down":
            targets = self[-1]
            neighbor_attribute = 'upper_neighbor'

        elif direction == "left":
            targets = [row[0] for row in self]
            neighbor_attribute = 'lower_neighbor'

        elif direction == "right":
            targets = [row[-1] for row in self]
            neighbor_attribute = 'lower_neighbor'

        else:
            raise ValueError('Shift direction must be up, down, left, or right')

        success = False
        for target in targets:
            if target.shift(neighbor_attribute):  # Returns True if this column moved, False if not
                success = True

        return success  # False is game over, True we are fine
