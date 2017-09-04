from collections import namedtuple


class Pile:
    def __init__(self, cards, x, y, card_size, pile_type="tableau"):
        self.Order = namedtuple('Order', ['foundation', 'rank', 'color_suit'])
        self.card_width, self.card_height = card_size
        self.draw_three = True

        self.pile_type = pile_type
        if self.pile_type == 'tableau':
            self.fanned = True
            self.order = self.Order(foundation='king', rank=-1, color_suit='alt-color')
            self.face_up = 'top'
            self.height = 500
        elif self.pile_type == 'foundation':
            self.fanned = False
            self.order = self.Order(foundation='ace', rank=1, color_suit='same-suit')
            self.face_up = 'all'
            self.height = self.card_height
        elif self.pile_type == 'wastepile':
            self.fanned = False
            self.order = self.Order(foundation=None, rank=None, color_suit=None)
            self.face_up = 'all'
            self.height = self.card_height
        elif self.pile_type == 'deck':
            self.fanned = False
            self.order = self.Order(foundation=None, rank=None, color_suit=None)
            self.face_up = 'none'
            self.height = self.card_height

        self.card_spacing = 40
        self.cards = cards
        self.x = x
        self.y = y

        self.update_positions()

    def update_positions(self):
        if len(self.cards) != 0:
            for index, card in enumerate(self.cards):
                if self.face_up == 'none':
                    card.face_up = False
                elif self.face_up == 'top':
                    if index == len(self.cards) - 1:
                        card.face_up = True
                elif self.face_up == 'all':
                    card.face_up = True

                if self.fanned == True:
                    card.position = (self.x, self.y + (index * self.card_spacing))
                else:
                    card.position = (self.x, self.y)

    def selected(self, mouse_position, piles):
        selection = False
        selected_cards = []
        deselect_pile = False

        for index, card in enumerate(self.cards):
                card_clicked = card.check_if_clicked(mouse_position)
                if card_clicked and card.face_up:
                    selection = True
                    selected_cards = self.cards[index:]

        if self.pile_type == 'deck':
            deselect_pile = True

            wastepile = None
            for pile in piles:
                if pile.pile_type == 'wastepile':
                    wastepile = pile
                    break

            if len(self.cards) != 0:
                if self.draw_three == True:
                    if len(self.cards) >= 3:
                        index_range = 3
                    elif len(self.cards) == 2:
                        index_range = 2
                    else:
                        index_range = 1

                    for _ in range(index_range):
                        wastepile.cards.append(self.cards[-1])
                        del self.cards[-1]
                else:
                    wastepile.cards.append(self.cards[-1])
                    del self.cards[-1]
            else:
                self.cards = wastepile.cards[::-1]
                wastepile.cards = []

        return selection, selected_cards, deselect_pile

    def valid_transfer(self, pile_to_transfer_to, selected_cards, ranks):
        if len(pile_to_transfer_to.cards) != 0:
            bottom_card = pile_to_transfer_to.cards[-1]
        else:
            bottom_card = None
        top_card = selected_cards[0]

        valid = True
        
        # cannot transfer to the deck
        if pile_to_transfer_to.pile_type == 'deck' or pile_to_transfer_to.pile_type == 'wastepile':
            valid = False

        # if a pile is empty only certain cards can be placed there
        if bottom_card == None:
            if pile_to_transfer_to.order.foundation != None:
                if top_card.rank != pile_to_transfer_to.order.foundation:
                    valid = False
        else:
            # cards must be ordered depending on the pile they are in
            if pile_to_transfer_to.order.rank != None:
                rank_index = ranks.index(bottom_card.rank)
                if top_card.rank != ranks[rank_index + pile_to_transfer_to.order.rank]:
                    valid = False
            if pile_to_transfer_to.order.color_suit != None:
                if pile_to_transfer_to.order.color_suit == 'alt-color':
                    if top_card.color == bottom_card.color:
                        valid = False
                elif pile_to_transfer_to.order.color_suit == 'same-suit':
                    if top_card.suit != bottom_card.suit:
                        valid = False

        return valid

    def transfer_cards(self, selected_cards, pile_to_transfer_to, ranks):
        if self.valid_transfer(pile_to_transfer_to, selected_cards, ranks):
            for card in selected_cards:
                pile_to_transfer_to.cards.append(card)
                self.cards.remove(card)

    def selection_rect(self, card):
        padding = 10
        rect_x = card.position[0] - padding
        rect_y = card.position[1] - padding

        card_index = self.cards.index(card)
        card_negative_index = card_index - len(self.cards) - 1
        distance_from_top = abs(card_negative_index)

        rect_w = card.card_size[0] + (padding * 2)
        rect_h = (self.card_spacing * (distance_from_top - 2)) + self.card_height + (padding * 2)

        return [rect_x, rect_y, rect_w, rect_h]

    def check_if_clicked(self, mouse_position):
        mouse_x, mouse_y = mouse_position

        if self.x < mouse_x < self.x + self.card_width and self.y < mouse_y < self.y + self.height:
            return True
        else:
            return False
