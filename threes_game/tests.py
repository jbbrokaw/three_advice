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
