from copy import deepcopy
from deck import CompressedDeck

class HistoryManager:
    def __init__(self, deck):
        self.current_deck = 0
        self.decks = []
        self.add_deck(deck)

    def add_deck(self, deck):
        self.decks.append(CompressedDeck(deepcopy(deck.piles)))

    def valid_move_made(self, deck):
        self.add_deck(deck)
        self.current_deck += 1

    def undo(self, deck):
        if self.current_deck > 0:
            del self.decks[-1]
            self.current_deck -= 1
            return deepcopy(self.decks[self.current_deck]).decompress(deck.card_images, deck.card_size)
        else:
            return deck
