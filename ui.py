import pygame


class Text:
    def __init__(self, display_dimensions, offsets, text, size, color, font="RobotoSlab-Regular", centered=True):
        self.display_width, self.display_height = display_dimensions
        self.x_offset, self.y_offset = offsets

        self.text = text
        self.size = size
        self.color = color
        self.font = pygame.font.Font("fonts/"+font+".ttf", self.size)
        self.centered = centered

    def display(self, game_display):
        text_surface = self.font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect()

        if self.centered:
            text_rect.center = (self.display_width//2 + self.x_offset, self.display_height//2 + self.y_offset)
            game_display.blit(text_surface, text_rect)
        else:
            game_display.blit(text_surface, [self.x_offset, self.y_offset])


class Button:
    def __init__(self, display_dimensions, text, offsets, dimensions, color, centered=True, action=None):
        self.display_width, self.display_height = display_dimensions
        self.x_offset, self.y_offset = offsets
        self.width, self.height = dimensions

        self.text = text
        self.color = color
        self.centered = centered
        self.action = action

    # TODO: display(with text rendering), click, and hover