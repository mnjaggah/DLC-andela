import unittest
from track import Challenge, Skill, Board

class TrackingBoardTest(unittest.TestCase):

    def test_challenge_isinstance(self):
        new_board = Board("Amity Space Allocation")
        new_skill = new_board.add_skill("Python Data Structures")
        new_challenge = new_skill.add_challenge("Lists and Dictionaries")
        self.assertEqual(new_board.name, "Amity Space Allocation")
        self.assertEqual(new_skill.name, "Python Data Structures")
        self.assertEqual(new_challenge.name, "Lists and Dictionaries")
        self.assertIsInstance(new_board, Board)
        self.assertIsInstance(new_skill, Skill)
        self.assertIsInstance(new_challenge, Challenge)

