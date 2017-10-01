from copy import deepcopy
from deck import Deck

class UndoManager:
    def __init__(self, deck):
        self.decks = [self.copy_piles(deck)]
        self.current_deck = 0

    def copy_piles(self, deck):
        piles = []
        for pile in deck.piles:
            piles.append(deepcopy(pile))
        return piles

    def add_deck(self, deck):
        print(len(self.decks))
        self.decks.append(self.copy_piles(deck))
        self.current_deck += 1
        print(len(self.decks))
        print(self.decks)
        if len(self.decks) > 1:
            print(self.decks[0] == self.decks[1])
            print(self.decks[0][0].cards[0] == self.decks[1][0].cards[0])

    def undo(self, deck):
        if self.current_deck > 0:
            print(self.decks)
            print(len(self.decks))
            self.current_deck -= 1

            del self.decks[-1]
            print(len(self.decks))
            print(self.decks)
            return Deck(self.copy_piles(Deck(self.decks[-1], deck.card_images, deck.card_size)), deck.card_images, deck.card_size)
        else:
            return deck
