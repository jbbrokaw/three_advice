from django.test import TestCase
from threes_game.gameplay import Board
# Create your tests here.

class GameplayTest(TestCase):
    def setUp(self):
        self.blank_board = Board()
        data = list()
        for n in xrange(4):
            data.append(range(4 * n, 4 * (n + 1)))

        self.populated_board = Board(data=data)

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
