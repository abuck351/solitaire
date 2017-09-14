import pygame
from deck import Deck
from ui import Text, Button, RadioGroup, Radio, Checkbox


white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 200, 0)
blue = (50, 50, 190)
red = (190, 50, 50)
grey = (100, 100, 100)

display_dimensions = (1100, 800)

pygame.init()

game_display = pygame.display.set_mode(display_dimensions)

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
    deck.load_piles(display_dimensions)

    while True:
        if deck.check_for_win():
            print("You win!!!")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_loop()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if event.button == 1:
                    piles_to_update = deck.handle_click(mouse_pos)
                    deck.update(piles_to_update, display_dimensions[1])
                if event.button == 3:
                    deck.handle_right_click(mouse_pos)

        game_display.fill(blue)
        deck.display(game_display)
        pygame.display.update()
        clock.tick(FPS)


def options_menu():
    title = Text(display_dimensions, (0, -350), "Options", 40, black)

    buttons = []
    buttons.append(Button(display_dimensions, "Back", (10, 10), (75, 25), red, centered=False, text_color=white, text_size=14, action="back"))

    radio1 = Radio(display_dimensions, (0, 0), checked=True)
    radio2 = Radio(display_dimensions, (0, 30))
    radio3 = Radio(display_dimensions, (0, 60))
    radiogroup1 = RadioGroup(radio1, radio2, radio3)

    checkbox1 = Checkbox(display_dimensions, (0, 100))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if event.button == 1:
                    for button in buttons:
                        if button.check_if_clicked(mouse_pos):
                            if button.action == "back":
                                start_menu()
                            else:
                                print("Button action: {} does not exist".format(button.action))

                    radiogroup1.check_if_clicked(mouse_pos)
                    checkbox1.check_if_clicked(mouse_pos)

        game_display.fill(white)

        title.display(game_display)
        radiogroup1.display(game_display)
        checkbox1.display(game_display)

        for button in buttons:
            button.display(game_display, pygame.mouse.get_pos())

        pygame.display.update()


def start_menu():
    title = Text(display_dimensions, (0, -100), "Solitaire", 50, black)

    buttons = []
    buttons.append(Button(display_dimensions, "Play", (0, 0), (100, 50), blue, text_color=white, text_size=26, action="start_game"))
    buttons.append(Button(display_dimensions, "Quit", (200, 0), (100, 50), red, text_color=white, action="quit"))
    buttons.append(Button(display_dimensions, "Options", (-200, 0), (100, 50), grey, text_color=white, action="options"))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if event.button == 1:
                    for button in buttons:
                        if button.check_if_clicked(mouse_pos):
                            if button.action == "start_game":
                                game_loop()
                            elif button.action == "quit":
                                quit_game()
                            elif button.action == "options":
                                options_menu()
                                pass
                            else:
                                print("Button action: {} does not exist".format(button.action))

        game_display.fill(white)

        title.display(game_display)

        for button in buttons:
            button.display(game_display, pygame.mouse.get_pos())

        pygame.display.update()


start_menu()
