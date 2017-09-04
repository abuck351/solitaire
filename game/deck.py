import os
import random
import pygame
from pile import Pile
from card import Card


# the deck class should handle the clicking of the cards
class Deck:
    def __init__(self):
        self.cards = []

        self.suits = ['clubs', 'diamonds', 'hearts', 'spades']
        self.ranks = ['ace', '2', '3', '4', '5', '6', '7', '8',
                      '9', '10', 'jack', 'queen', 'king']

        self.selection = False
        self.selected_cards = []
        self.selected_pile = None

        self.selection_rect = None
        self.selection_color = (255, 255, 0)
        self.empty_color = (100, 100, 200)

        self.card_size = (100, 150)
        name_of_image = os.path.join('resources', 'card_back.png')
        self.card_back = pygame.image.load(name_of_image)
        self.card_back = pygame.transform.scale(self.card_back, self.card_size)

        self.piles = []

    def load_cards(self):
        for suit in self.suits:
            for rank in self.ranks:
                name_of_image = os.path.join('resources', 'cards', '{}_of_{}.png'.format(rank, suit))
                img = pygame.image.load(name_of_image)
                img = pygame.transform.scale(img, self.card_size)

                self.cards.append(Card(img, self.card_back, self.card_size, rank, suit))

    def load_piles(self, display_size):
        display_width, display_height = display_size
        pile_spacing = 50

        start_x = 50
        start_y = self.card_size[1] + 100

        foundation_x_step = self.card_size[0] + pile_spacing
        foundation_start_x = display_width - (foundation_x_step * 4)

        # tableau piles
        self.piles.append(Pile([self.cards[0]], start_x, start_y, self.card_size))
        self.piles.append(Pile(self.cards[1:3], start_x + self.card_size[0] + pile_spacing, start_y, self.card_size))
        self.piles.append(Pile(self.cards[3:6], start_x + self.card_size[0]*2 + pile_spacing*2, start_y, self.card_size))
        self.piles.append(Pile(self.cards[6:10], start_x + self.card_size[0]*3 + pile_spacing*3, start_y, self.card_size))
        self.piles.append(Pile(self.cards[10:15], start_x + self.card_size[0]*4 + pile_spacing*4, start_y, self.card_size))
        self.piles.append(Pile(self.cards[15:21], start_x + self.card_size[0]*5 + pile_spacing*5, start_y, self.card_size))
        self.piles.append(Pile(self.cards[21:28], start_x + self.card_size[0]*6 + pile_spacing*6, start_y, self.card_size))

        self.piles.append(Pile(self.cards[28:], start_x, pile_spacing, self.card_size, pile_type="deck"))
        self.piles.append(Pile([], start_x + self.card_size[0] + pile_spacing, pile_spacing, self.card_size, pile_type="wastepile"))

        self.piles.append(Pile([], foundation_start_x, pile_spacing, self.card_size, pile_type="foundation"))
        self.piles.append(Pile([], foundation_start_x + foundation_x_step, pile_spacing, self.card_size, pile_type="foundation"))
        self.piles.append(Pile([], foundation_start_x + foundation_x_step*2, pile_spacing, self.card_size, pile_type="foundation"))
        self.piles.append(Pile([], foundation_start_x + foundation_x_step*3, pile_spacing, self.card_size, pile_type="foundation"))

    def shuffle_cards(self):
        random.shuffle(self.cards)

    def deselect(self):
        self.selection = False
        self.selected_pile = None
        self.selected_cards = []

    def which_pile_clicked(self, mouse_position):
        for pile in self.piles:
                if pile.check_if_clicked(mouse_position):
                    return pile
        else:
            return None

    def handle_click(self, mouse_position):
        if self.selection == False:
            # the player selects card/s
            self.selected_pile = self.which_pile_clicked(mouse_position)
            if self.selected_pile != None:
                self.selection, self.selected_cards, deselect_pile = self.selected_pile.selected(mouse_position, self.piles)
                if deselect_pile:
                    self.deselect()
                else:
                    if len(self.selected_cards) != 0:
                        self.selection_rect = self.selected_pile.selection_rect(self.selected_cards[0])
        else:
            pile_to_transfer_to = self.which_pile_clicked(mouse_position)
            if self.selected_pile != None and pile_to_transfer_to != None:
                self.selected_pile.transfer_cards(self.selected_cards, pile_to_transfer_to, self.ranks)
            self.deselect()

        for pile in self.piles:
            pile.update_positions()

    def handle_right_click(self, mouse_position):
        self.deselect()

    def check_for_win(self):
        foundation_piles = [pile for pile in self.piles if pile.pile_type == 'foundation']
        for pile in foundation_piles:
            if len(pile.cards) < 13:
                return False
        else:
            return True

    def display(self, game_display):
        for pile in self.piles:
            if pile.pile_type == 'foundation' or pile.pile_type == 'deck' and len(pile.cards) == 0:
                pygame.draw.rect(game_display, self.empty_color, [pile.x, pile.y, pile.card_width, pile.card_height])
            for card in pile.cards:
                if self.selection and self.selection_rect != None and card == self.selected_cards[0]:
                    pygame.draw.rect(game_display, self.selection_color, self.selection_rect)
                img, x, y = card.display_info()
                game_display.blit(img, [x, y])

