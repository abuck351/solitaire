import unittest

from deck import Deck


class SolitaireTests(unittest.TestCase):

    def setUp(self):
        self.deck = Deck()
        self.deck.load_cards()

    def test_deck_size(self):
        self.assertEqual(len(self.deck.cards), 52)
        self.deck.shuffle_cards()
        self.assertEqual(len(self.deck.cards), 52)

    def test_pile_sizes(self):
        self.deck.load_piles()
        self.assertEqual(len(self.deck.piles[0].cards), 1)
        self.assertEqual(len(self.deck.piles[1].cards), 2)
        self.assertEqual(len(self.deck.piles[2].cards), 3)
        self.assertEqual(len(self.deck.piles[3].cards), 4)
        self.assertEqual(len(self.deck.piles[4].cards), 5)
        self.assertEqual(len(self.deck.piles[5].cards), 6)
        self.assertEqual(len(self.deck.piles[6].cards), 7)

        self.assertEqual(len(self.deck.piles[7].cards), 24)


if __name__ == '__main__':
    unittest.main()
