class Pile:
    def __init__(self, cards, x, y, pile_type="tableau"):
        self.pile_type = pile_type

        self.card_spacing = 40

        self.x = x
        self.y = y

        self.cards = cards

        if pile_type == "tableau":
            self.cards[-1].face_up = True
            for index, card in enumerate(self.cards):
                card.position = (self.x, self.y + (index * self.card_spacing))
        if pile_type == "stock":
            for card in self.cards:
                card.position = (self.x, self.y)

    def selected_cards_info(self, card):
        padding = 10
        rect_x = card.position[0] - padding
        rect_y = card.position[1] - padding

        card_index = self.cards.index(card)
        card_negative_index = card_index - len(self.cards) - 1
        distance_from_top = abs(card_negative_index)

        rect_w = card.card_size[0] + (padding * 2)
        rect_h = (self.card_spacing * (distance_from_top - 2)) + card.card_size[1] + (padding * 2)

        return [rect_x, rect_y, rect_w, rect_h]

