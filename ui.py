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
    #TODO: make buttons clickable, display button text, button actions
    def __init__(self, display_dimensions, text, offsets, dimensions, color, centered=True, action=None):
        self.display_width, self.display_height = display_dimensions
        self.x_offset, self.y_offset = offsets
        self.width, self.height = dimensions

        self.text = text
        self.color = color
        self.highlight_strength = 20
        self.centered = centered
        self.action = action

    @property
    def x(self):
        if self.centered:
            return ((self.display_width//2) - (self.width//2)) + self.x_offset
        else:
            return self.x_offset

    @property
    def y(self):
        if self.centered:
            return ((self.display_width//2) - (self.height//2)) + self.y_offset
        else:
            return self.y_offset

    def check_for_mouse_over(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        if self.x < mouse_x < self.x + self.width and self.y < mouse_y < self.y + self.height:
            return True
        else:
            return False

    def highlight_color(self):
        color_value_list = list(self.color)
        for index, color_value in enumerate(color_value_list):
            color_value += self.highlight_strength
            if color_value > 255:
                color_value = 255
            color_value_list[index] = color_value
        return tuple(color_value_list)

    def display(self, game_display, mouse_pos):
        if self.check_for_mouse_over(mouse_pos):
            button_color = self.highlight_color()
        else:
            button_color = self.color

        pygame.draw.rect(game_display, button_color, [self.x, self.y, self.width, self.height])
