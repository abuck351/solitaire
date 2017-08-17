# https://en.wikipedia.org/wiki/Glossary_of_patience_terms
import pygame
from deck import Deck


white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 200, 0)

pygame.init()

display_width = 1200
display_height = 1000
game_display = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption('Solitare')

clock = pygame.time.Clock()


def quit_game():
    pygame.quit()
    quit()


def game_loop():
    FPS = 10
    #import pdb; pdb.set_trace()

    deck = Deck()
    deck.load_cards()
    deck.shuffle_cards()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_loop()

        game_display.fill(green)
        deck.display(game_display)
        pygame.display.update()
        clock.tick(FPS)


game_loop()
