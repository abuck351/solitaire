import random


class Card:
    def __init__(self, img, card_back, rank, suit, face_up=False):
        self.img = img
        self.card_back = card_back
        self.suit = suit

        if self.suit == 'diamonds' or self.suit == 'hearts':
            self.color = 'red'
        elif self.suit == 'spades' or self.suit == 'clubs':
            self.color = 'black'

        self.rank = rank
        self.face_up = face_up

        # TODO: location must be assigned to the card, not just random
        self.location = (random.randint(0, 1100), random.randint(0, 900))

    def display(self):
        if self.face_up:
            # show the card face
            return self.img, self.location[0], self.location[1]
        else:
            # show the back of the card
            return self.card_back, self.location[0], self.location[1]
