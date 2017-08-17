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


if __name__ == '__main__':
    unittest.main()
