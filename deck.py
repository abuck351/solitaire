import random
import pygame
from card import Card


# the deck class should handle the clicking of the cards
class Deck:
    def __init__(self):
        self.cards = []

        self.card_size = (100, 150)
        self.card_back = pygame.image.load('card_back.png')
        self.card_back = pygame.transform.scale(self.card_back, self.card_size)

    def load_cards(self):
        suits = ['clubs', 'diamonds', 'hearts', 'spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9',
                 '10', 'ace', 'jack', 'queen', 'king']
        for suit in suits:
            for rank in ranks:
                img = pygame.image.load('cards\{}_of_{}.png'.format(rank, suit))
                img = pygame.transform.scale(img, self.card_size)

                self.cards.append(Card(img, self.card_back, rank, suit, face_up=True))

    def shuffle_cards(self):
        random.shuffle(self.cards)

    def display(self, game_display):
        for card in self.cards:
            img, x, y = card.display()
            game_display.blit(img, [x, y])

