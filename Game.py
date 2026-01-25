import pygame
import pygame_menu
pygame.init()


# Settings



# Sets the selected gamemode in the menu 
current_gamemode = 1
def set_gamemode(value, gamemode):
    global current_gamemode
    current_gamemode = gamemode
    

def start_the_game():
    print(current_gamemode)
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
menu.add.selector('Gamemode :', [('<Vocabulary>', 0), ('←Grammer→', 1), ('←Test→', 2)], onchange=set_gamemode)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)



# Main loop
menu.mainloop(screen)









