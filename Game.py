import pygame
import pygame_menu
pygame.init()


# Settings


def set_difficulty(value, difficulty):
    # Do the job here !
    pass

def start_the_game():
    # Do the job here !
    pass

# Screen setup
screen = pygame.display.set_mode((1100,500),0,32)
pygame.display.set_caption("Learning Urdu")

# Theme
font = pygame_menu.font.FONT_8BIT
mytheme = pygame_menu.themes.THEME_DARK
mytheme.widget_font = font


# Menu Setup
menu = pygame_menu.Menu('Welcome', 800, 500, theme=mytheme)

menu.add.text_input('PLEASE ENTER NAME :', default='')
menu.add.selector('Gamemode :', [('<Vocabulary>', 1), ('←Grammer→', 2), ('←Test→', 3)], onchange=set_difficulty)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)



# Main loop
menu.mainloop(screen)









