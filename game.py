import pygame
from deck import Deck


white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 200, 0)

display_width = 1100
display_height = 800

pygame.init()

game_display = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption('Solitare')

clock = pygame.time.Clock()


def quit_game():
    pygame.quit()
    quit()


def game_loop():
    FPS = 10

    deck = Deck()
    deck.load_cards()
    deck.shuffle_cards()
    deck.load_piles((display_width, display_height))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_loop()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if event.button == 1:
                    deck.handle_click((mouse_x, mouse_y))
                if event.button == 3:
                    deck.handle_right_click((mouse_x, mouse_y))

        game_display.fill(green)
        deck.display(game_display)
        pygame.display.update()
        clock.tick(FPS)


game_loop()
