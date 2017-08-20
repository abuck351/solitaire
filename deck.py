import random
import pygame
from pile import Pile
from card import Card


# the deck class should handle the clicking of the cards
class Deck:
    def __init__(self):
        self.cards = []

        self.selected_card = None
        self.selected_cards = []
        self.selected_pile = None
        self.selection_rect = None
        self.selection_color = (255, 255, 0)

        self.card_size = (100, 150)
        self.card_back = pygame.image.load('card_back.png')
        self.card_back = pygame.transform.scale(self.card_back, self.card_size)

        self.piles = []

    def load_cards(self):
        suits = ['clubs', 'diamonds', 'hearts', 'spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9',
                 '10', 'ace', 'jack', 'queen', 'king']
        for suit in suits:
            for rank in ranks:
                img = pygame.image.load('cards\{}_of_{}.png'.format(rank, suit))
                img = pygame.transform.scale(img, self.card_size)

                self.cards.append(Card(img, self.card_back, self.card_size, rank, suit))

    def load_piles(self):
        # TODO: Try not to hard code the x, y values
        start_x = 50
        start_y = self.card_size[1] + 100
        pile_spacing = 50

        # tableau piles
        self.piles.append(Pile([self.cards[0]], start_x, start_y))
        self.piles.append(Pile(self.cards[1:3], start_x + self.card_size[0] + pile_spacing, start_y))
        self.piles.append(Pile(self.cards[3:6], start_x + self.card_size[0]*2 + pile_spacing*2, start_y))
        self.piles.append(Pile(self.cards[6:10], start_x + self.card_size[0]*3 + pile_spacing*3, start_y))
        self.piles.append(Pile(self.cards[10:15], start_x + self.card_size[0]*4 + pile_spacing*4, start_y))
        self.piles.append(Pile(self.cards[15:21], start_x + self.card_size[0]*5 + pile_spacing*5, start_y))
        self.piles.append(Pile(self.cards[21:28], start_x + self.card_size[0]*6 + pile_spacing*6, start_y))

        # stock pile
        self.piles.append(Pile(self.cards[28:], start_x, 50, pile_type="stock"))

        # TODO: still need the empty foundation piles

    def shuffle_cards(self):
        random.shuffle(self.cards)

    def deselect(self):
        self.selected_card = None
        self.selected_pile = None
        self.selected_cards = []

    def handle_click(self, mouse_position):
        if self.selected_card == None:
            for pile in self.piles:
                for index, card in enumerate(pile.cards):
                    card_clicked = card.check_if_clicked(mouse_position)
                    if card_clicked and card.face_up:
                        self.selected_card = card
                        self.selected_cards = pile.cards[index:]
                        self.selected_pile = pile
        else:
            # this is where the player chooses where to place the card
            pile_to_place_cards = None
            for pile in self.piles:
                if pile.pile_type == "tableau" or pile.pile_type == "foundation":
                    pile_clicked = pile.check_if_clicked(mouse_position, self.selected_cards[0].card_size[0])
                    if pile_clicked:
                        pile_to_place_cards = pile
            if pile_to_place_cards != None:
                for card in self.selected_cards:
                    self.selected_pile.cards.remove(card)
                    pile_to_place_cards.cards.append(card)

                for pile in self.piles:
                    pile.card_positions()

                if len(self.selected_pile.cards) != 0:
                    self.selected_pile.cards[-1].face_up = True

            self.deselect()
            

        if self.selected_card != None:
            self.selection_rect = self.selected_pile.selected_cards_info(self.selected_card)

        print(str(self.selected_cards))

    def handle_right_click(self, mouse_position):
        self.deselect()

    def display(self, game_display):
        for pile in self.piles:
            for card in pile.cards:
                if card == self.selected_card:
                    if self.selection_rect != None:
                        pygame.draw.rect(game_display, self.selection_color, self.selection_rect)
                img, x, y = card.display_info()
                game_display.blit(img, [x, y])

