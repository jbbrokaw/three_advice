from django.test import TestCase
from threes_game.gameplay import Board

class GameplayTest(TestCase):
    def setUp(self):
        self.blank_board = Board()
        data = list()
        for n in xrange(4):
            data.append(range(4 * n, 4 * (n + 1)))

        self.populated_board = Board(data=data)

        test_data = \
            [[  3,   3,   2,  24],
             [  2,  24,   6,   3],
             [  2,  96,   1,   6],
             [384,  24,   1,   1]]
        self.test_board = Board(data=test_data)
        left_shifted_data = \
            [[  6,   2,  24,  None],
             [  2,  24,   6,   3],
             [  2,  96,   1,   6],
             [384,  24,   1,   1]]
        self.left_shifted_board = Board(data=left_shifted_data)
        right_shifted_data = \
            [[None,  6,   2,  24],
             [  2,  24,   6,   3],
             [  2,  96,   1,   6],
             [384,  24,   1,   1]]
        self.right_shifted_board = Board(data=right_shifted_data)

    def test_board_values(self):
        for value_row in self.blank_board.values:
            for value in value_row:
                self.assertIsNone(value)

        i = 0
        for value_row in self.populated_board.values:
            for value in value_row:
                self.assertEqual(value, i)
                i += 1

    def test_neighbors(self):
        top_left_tile = self.populated_board[0][0]
        self.assertEqual(top_left_tile.value, 0)
        self.assertIsNone(top_left_tile.upper_neighbor)
        self.assertIsNone(top_left_tile.left_neighbor)
        self.assertEqual(top_left_tile.right_neighbor.value, 1)
        self.assertEqual(top_left_tile.lower_neighbor.value, 4)

        bottom_right_tile = self.populated_board[3][3]
        self.assertEqual(bottom_right_tile.value, 15)
        self.assertIsNone(bottom_right_tile.right_neighbor)
        self.assertIsNone(bottom_right_tile.lower_neighbor)
        self.assertEqual(bottom_right_tile.left_neighbor.value, 14)
        self.assertEqual(bottom_right_tile.upper_neighbor.value, 11)

        right_edge_tile = self.populated_board[1][3]
        self.assertEqual(len(right_edge_tile.neighbors), 3)
        self.assertIn(self.populated_board[1][2], right_edge_tile.neighbors)
        self.assertIn(self.populated_board[0][3], right_edge_tile.neighbors)
        self.assertIn(self.populated_board[2][3], right_edge_tile.neighbors)

    def test_shifts(self):
        self.assertRaises(ValueError, self.test_board.shift, 'diagonal')
        self.assertFalse(self.test_board.shift('down'))
        self.assertFalse(self.test_board.shift('up'))
        original_data = self.test_board.values

        self.assertTrue(self.test_board.shift('left'))
        for row in xrange(4):
            for col in xrange(4):
                self.assertEqual(self.test_board.values[row][col],
                                 self.left_shifted_board.values[row][col])
        self.assertFalse(self.test_board.shift('left'))

        # Reset and test right shift
        self.test_board = Board(original_data)
        self.assertTrue(self.test_board.shift('right'))
        for row in xrange(4):
            for col in xrange(4):
                self.assertEqual(self.test_board.values[row][col],
                                 self.right_shifted_board.values[row][col])
        self.assertFalse(self.test_board.shift('right'))
