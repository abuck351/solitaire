import random


class Card:
    def __init__(self, name_of_image, card_size, rank, suit, face_up=False):
        self.name_of_image = name_of_image
        self.card_size = card_size
        self.suit = suit
        self.rank = rank
        self.face_up = face_up

        if self.suit == 'diamonds' or self.suit == 'hearts':
            self.color = 'red'
        elif self.suit == 'spades' or self.suit == 'clubs':
            self.color = 'black'

        self.position = (0, 0)

    @property
    def x(self):
        return self.position[0]

    @property
    def y(self):
        return self.position[1]

    def check_if_clicked(self, mouse_position):
        width, height = self.card_size
        mouse_x, mouse_y = mouse_position

        if self.x < mouse_x < self.x + width and self.y < mouse_y < self.y + height:
            return True
        else:
            return False

    def __str__(self):
        return "{} of {}".format(self.rank, self.suit)

    def __repr__(self):
        return self.__str__()
