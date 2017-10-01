import os
import random
import pygame
from itertools import count
from pile import Pile
from card import Card


# the deck class should handle the clicking of the cards
class Deck:
    def __init__(self, piles=[], card_images={}, card_size=(100, 150)):
        # cards list is only used when starting/restarting a game
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

        # these attributes can be modified when undoing/redoing
        self.piles = piles
        self.card_images = card_images
        self.card_size = card_size

        name_of_image = os.path.join('resources', 'card_back.png')
        self.card_back_image = pygame.image.load(name_of_image)
        self.card_back = self.resize_card_back()

    def resize_card_back(self):
        return pygame.transform.scale(self.card_back_image, self.card_size)

    def resize_card_images(self):
        for name_of_image, card_image in self.card_images.items():
            self.card_images[name_of_image] = pygame.transform.scale(card_image, self.card_size)

    def load_cards(self):
        for suit in self.suits:
            for rank in self.ranks:
                name_of_image = os.path.join('resources', 'cards', '{}_of_{}.png'.format(rank, suit))
                self.card_images[name_of_image] = pygame.image.load(name_of_image)
                self.cards.append(Card(name_of_image, self.card_size, rank, suit))
        self.resize_card_images()

    def load_piles(self, display_size):
        display_width, display_height = display_size
        pile_spacing = 50

        start_x = 50
        start_y = self.card_size[1] + 100

        foundation_x_step = self.card_size[0] + pile_spacing
        foundation_start_x = display_width - (foundation_x_step * 4)

        tableau1 = Pile([self.cards[0]], start_x, start_y, self.card_size)
        tableau2 = Pile(self.cards[1:3], start_x + self.card_size[0] + pile_spacing, start_y, self.card_size)
        tableau3 = Pile(self.cards[3:6], start_x + self.card_size[0]*2 + pile_spacing*2, start_y, self.card_size)
        tableau4 = Pile(self.cards[6:10], start_x + self.card_size[0]*3 + pile_spacing*3, start_y, self.card_size)
        tableau5 = Pile(self.cards[10:15], start_x + self.card_size[0]*4 + pile_spacing*4, start_y, self.card_size)
        tableau6 = Pile(self.cards[15:21], start_x + self.card_size[0]*5 + pile_spacing*5, start_y, self.card_size)
        tableau7 = Pile(self.cards[21:28], start_x + self.card_size[0]*6 + pile_spacing*6, start_y, self.card_size)

        stock = Pile(self.cards[28:], start_x, pile_spacing, self.card_size, pile_type="stock")
        waste = Pile([], start_x + self.card_size[0] + pile_spacing, pile_spacing, self.card_size, pile_type="waste")

        foundation1 = Pile([], foundation_start_x, pile_spacing, self.card_size, pile_type="foundation")
        foundation2 = Pile([], foundation_start_x + foundation_x_step, pile_spacing, self.card_size, pile_type="foundation")
        foundation3 = Pile([], foundation_start_x + foundation_x_step*2, pile_spacing, self.card_size, pile_type="foundation")
        foundation4 = Pile([], foundation_start_x + foundation_x_step*3, pile_spacing, self.card_size, pile_type="foundation")

        self.piles = [tableau1, tableau2, tableau3, tableau4, tableau5, tableau6, tableau7,
                      stock, waste,
                      foundation1, foundation2, foundation3, foundation4]

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

    def update(self, piles_to_update, display_height):
        for pile in self.piles:
            pile.update()

        if piles_to_update != None:
            for pile in piles_to_update:
                pile.fit_pile_to_screen(display_height)
                pile.update_positions()

    def handle_click(self, mouse_position):
        piles_to_update = None
        valid_move = False

        if self.selection == False:
            # the player selects card/s
            self.selected_pile = self.which_pile_clicked(mouse_position)

            if self.selected_pile != None:
                if self.selected_pile.pile_type == 'stock':
                    valid_move = True

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
                valid_move = self.selected_pile.transfer_cards(self.selected_cards, pile_to_transfer_to, self.ranks)
                piles_to_update = self.selected_pile, pile_to_transfer_to
            else:
                piles_to_update = None

            self.deselect()
        
        return piles_to_update, valid_move

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

                if card.face_up:  
                    img = self.card_images[card.name_of_image]
                else:
                    img = self.card_back

                game_display.blit(img, [card.x, card.y])


class CompressedDeck:
    _ids = count(0)

    def __init__(self, piles):
        self.id = next(self._ids)
        self.piles = piles

    def decompress(self, card_images, card_size):
        return Deck(self.piles, card_images, card_size)

    def __str__(self):
        return str([card for card in self.piles if card.face_up == True])

    def __repr__(self):
        return "CompressedDeck #{}".format(self.id)
