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
            text_rect.center = (self.display_width//2, self.display_height//2)

        game_display.blit(text_surface, text_rect)


class Button:
    def __init__(self, display_dimensions, offsets, dimensions, color, centered=True, action=None):
        self.display_width, self.display_height = display_dimensions
        self.x_offset, self.y_offset = offsets
        self.width, self.height = dimensions

        self.color = color
        self.centered = centered
        self.action = action