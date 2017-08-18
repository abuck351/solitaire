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