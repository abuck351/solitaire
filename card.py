import random


class Card:
    def __init__(self, img, card_back, card_size, rank, suit, face_up=False):
        self.img = img
        self.card_back = card_back
        self.card_size = card_size
        self.suit = suit
        self.rank = rank
        self.face_up = face_up

        if self.suit == 'diamonds' or self.suit == 'hearts':
            self.color = 'red'
        elif self.suit == 'spades' or self.suit == 'clubs':
            self.color = 'black'

        self.position = (0, 0)

    def check_if_clicked(self, mouse_position):
        x, y = self.position
        width, height = self.card_size
        mouse_x, mouse_y = mouse_position

        if x < mouse_x < x + width and y < mouse_y < y + height:
            return True
        else:
            return False

    def display_info(self):
        if self.face_up:
            # show the card face
            return self.img, self.position[0], self.position[1]
        else:
            # show the back of the card
            return self.card_back, self.position[0], self.position[1]

    def __str__(self):
        return "{} of {}".format(self.rank, self.suit)

    def __repr__(self):
        return self.__str__()
