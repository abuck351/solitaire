import unittest

from deck import Deck


class SolitaireTests(unittest.TestCase):

    def setUp(self):
        self.deck = Deck()
        self.deck.load_cards()
        self.deck.shuffle_cards()
        # TODO: Try to find a way not to hardcode the width and height
        self.deck.load_piles((1100, 800))

    def test_deck_size(self):
        self.assertEqual(len(self.deck.cards), 52)

    def test_pile_sizes(self):
        self.assertEqual(len(self.deck.piles[0].cards), 1)
        self.assertEqual(len(self.deck.piles[1].cards), 2)
        self.assertEqual(len(self.deck.piles[2].cards), 3)
        self.assertEqual(len(self.deck.piles[3].cards), 4)
        self.assertEqual(len(self.deck.piles[4].cards), 5)
        self.assertEqual(len(self.deck.piles[5].cards), 6)
        self.assertEqual(len(self.deck.piles[6].cards), 7)

        self.assertEqual(len(self.deck.piles[7].cards), 24)

    def test_pile_selection(self):
        cards = self.deck.piles[6].cards

        for card in cards:
            card.face_up = True

        click_position = (cards[0].position[0] + 10, cards[0].position[1] + 10)
        self.deck.handle_click(click_position)
        self.assertEqual(cards, self.deck.selected_cards)


if __name__ == '__main__':
    unittest.main()
