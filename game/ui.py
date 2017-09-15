import os
import pygame
from math import sqrt

check_img = pygame.image.load(os.path.join('resources', 'check.png'))


class Text:
    def __init__(self, display_dimensions, offsets, text, size, color, font="RobotoSlab-Regular", centered=True):
        self.display_width, self.display_height = display_dimensions
        self.x_offset, self.y_offset = offsets

        self.text = text
        self.size = size
        self.color = color
        name_of_font = os.path.join('resources', 'fonts', font + '.ttf')
        self.font = pygame.font.Font(name_of_font, self.size)
        self.centered = centered

    def text_objects(self):
        text_surface = self.font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect()
        return text_surface, text_rect

    def display(self, game_display):
        text_surface, text_rect = self.text_objects()

        if self.centered:
            text_rect.center = (self.display_width//2 + self.x_offset, self.display_height//2 + self.y_offset)
            game_display.blit(text_surface, text_rect)
        else:
            game_display.blit(text_surface, [self.x_offset, self.y_offset])

    def button_text_display(self, game_display, button_info):
        text_surface, text_rect = self.text_objects()
        x, y, width, height = button_info

        text_rect.center = (x + width//2, y + height//2)
        game_display.blit(text_surface, text_rect)        


class Button:
    def __init__(self, display_dimensions, text, offsets, dimensions, color, text_size=16, text_color=(0, 0, 0), enabled=True, centered=True, action=None):
        self.display_width, self.display_height = display_dimensions
        self.x_offset, self.y_offset = offsets
        self.width, self.height = dimensions

        self.enabled = enabled
        self.disabled_color = (200, 200, 200)
        self.disabled_text_color = (230, 230, 230)

        self.text = text

        self.text_color = text_color
        if self.enabled == False:
            text_display_color = self.disabled_color
        else:
            text_display_color = self.text_color
        self.text_object = Text(display_dimensions, (0, 0), text, text_size, text_display_color, centered=False)

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

    def check_if_clicked(self, mouse_pos):
        if self.check_for_mouse_over(mouse_pos) and self.enabled:
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
        if self.enabled:
            self.text_object.color = self.text_color
            if self.check_for_mouse_over(mouse_pos):
                button_color = self.highlight_color()
            else:
                button_color = self.color
        else:
            button_color = self.disabled_color
            self.text_object.color = self.disabled_text_color

        button_info = (self.x, self.y, self.width, self.height)

        pygame.draw.rect(game_display, button_color, list(button_info))

        self.text_object.button_text_display(game_display, button_info)


class RadioGroup:
    def __init__(self, *args):
        self.radios = list(args)

    def __iter__(self):
        return iter(self.radios)

    def check_if_clicked(self, mouse_pos):
        for radio in self.radios:
            radio.check_if_clicked(mouse_pos, self)

    def display(self, game_display):
        for radio in self.radios:
            radio.display(game_display)


class Radio:
    def __init__(self, display_dimensions, offsets, centered=True, checked=False, enabled=True):
        self.display_width, self.display_height = display_dimensions
        self.x_offset, self.y_offset = offsets
        self.centered = centered
        self.checked = checked
        self.enabled = enabled

        # even numbers only
        self.size = 10
        self.margin = 4

        self.color = (200, 200, 200)
        self.checked_color = (50, 50, 50)

    @property
    def x(self):
        if self.centered:
            return (self.display_width//2) + self.x_offset
        else:
            return self.x_offset

    @property
    def y(self):
        if self.centered:
            return (self.display_width//2) + self.y_offset
        else:
            return self.y_offset

    def check_for_mouse_over(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        x_dist = abs(self.x - mouse_x)
        y_dist = abs(self.y - mouse_y)
        distance = sqrt(x_dist**2 + y_dist**2)

        if distance < self.size:
            return True
        else:
            return False

    def check_if_clicked(self, mouse_pos, radio_group):
        if self.check_for_mouse_over(mouse_pos) and self.enabled:
            if radio_group != None:
                for radio in radio_group:
                    if radio != self:
                        radio.checked = False
                    else:
                        radio.checked = True

    def display(self, game_display):
        # TODO: display differently when disabled
        pygame.draw.circle(game_display, self.color, (self.x, self.y), self.size)

        if self.checked == True:
            pygame.draw.circle(game_display, self.checked_color, (self.x, self.y), self.size - self.margin)


class Checkbox:
    def __init__(self, display_dimensions, offsets, centered=True, checked=False, enabled=True):
        self.display_width, self.display_height = display_dimensions
        self.x_offset, self.y_offset = offsets
        self.centered = centered
        self.checked = checked
        self.enabled = enabled

        self.size = 20
        self.checkmark = check_img

        self.color = (200, 200, 200)
        self.checked_color = (50, 50, 50)

    @property
    def x(self):
        if self.centered:
            return ((self.display_width//2) - (self.size//2)) + self.x_offset
        else:
            return self.x_offset

    @property
    def y(self):
        if self.centered:
            return ((self.display_height//2) - (self.size//2)) + self.y_offset
        else:
            return self.y_offset

    def check_for_mouse_over(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        if self.x < mouse_x < self.x + self.size and self.y < mouse_y < self.y + self.size:
            return True
        else:
            return False 

    def check_if_clicked(self, mouse_pos):
        if self.check_for_mouse_over(mouse_pos) and self.enabled:
            self.checked = not self.checked

    def display(self, game_display):
        # TODO: display differently when disabled
        pygame.draw.rect(game_display, self.color, [self.x, self.y, self.size, self.size])

        if self.checked == True:
            self.checkmark = pygame.transform.scale(self.checkmark, (self.size, self.size))
            game_display.blit(self.checkmark, [self.x, self.y])
