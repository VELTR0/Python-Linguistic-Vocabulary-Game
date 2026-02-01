import pygame
import pygame_menu
from Game import startGame

pygame.init()


# Sets the selected gamemode in the menu 
current_gamemode = 1
def set_gamemode(value, gamemode):
    global current_gamemode
    current_gamemode = gamemode
    

def start_the_game():
    player_name = name.get_value()  
    menu.disable()
    player_name = "Player" if player_name == '' else player_name
    startGame(current_gamemode, screen, menu, mytheme, player_name )

# Screen setup
screen = pygame.display.set_mode((1024, 768),0,32)
pygame.display.set_caption("Learning Urdu")

# Theme
font = pygame_menu.font.FONT_8BIT
mytheme = pygame_menu.themes.THEME_DARK
mytheme.widget_font = font


# Menu Setup
menu = pygame_menu.Menu('Welcome', 1024, 768, theme=mytheme)

name = menu.add.text_input('PLEASE ENTER NAME :', default='')
menu.add.selector('Gamemode :', [('<Vocabulary>', 1), ('←Grammer→', 2), ('←Test→', 3)], onchange=set_gamemode)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)



# Main loop
menu.mainloop(screen)